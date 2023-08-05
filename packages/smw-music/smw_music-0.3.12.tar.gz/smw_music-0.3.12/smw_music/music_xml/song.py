# SPDX-FileCopyrightText: 2021 The SMW Music Python Project Authors
# <https://github.com/com-posers-pit/smw_music/blob/develop/AUTHORS.rst>
#
# SPDX-License-Identifier: AGPL-3.0-only

"""Song from MusicXML file."""

###############################################################################
# Imports
###############################################################################

# Standard library imports
import copy
import pkgutil
from datetime import datetime
from pathlib import PurePosixPath

# Library imports
import music21
from mako.template import Template  # type: ignore

# Package imports
from smw_music import __version__
from smw_music.music_xml.channel import Channel
from smw_music.music_xml.echo import EchoConfig
from smw_music.music_xml.instrument import (
    Dynamics,
    InstrumentConfig,
    InstrumentSample,
    NoteHead,
    SampleSource,
    dedupe_notes,
)
from smw_music.music_xml.reduction import reduce, remove_unused_instruments
from smw_music.music_xml.shared import CRLF, MusicXmlException
from smw_music.music_xml.tokens import (
    Annotation,
    Clef,
    CrescDelim,
    Crescendo,
    Dynamic,
    Error,
    Instrument,
    LoopDelim,
    Measure,
    Note,
    RehearsalMark,
    Repeat,
    Rest,
    Slur,
    Tempo,
    Token,
    Triplet,
    Vibrato,
)

###############################################################################
# Private function definitions
###############################################################################


def _get_cresc(
    part: music21.stream.Part,
) -> tuple[list[list[int]], list[bool]]:
    cresc: list[list[int]] = [[], []]
    cresc_list = list(filter(_is_crescendo, part))
    cresc[0] = [x.getFirst().id for x in cresc_list]
    cresc[1] = [x.getLast().id for x in cresc_list]
    cresc_type = [
        isinstance(x, music21.dynamics.Crescendo) for x in cresc_list
    ]

    return (cresc, cresc_type)


###############################################################################


def _get_lines(part: music21.stream.Part) -> list[list[int]]:
    lines: list[list[int]] = [[], []]
    line_list = list(filter(_is_line, part))
    lines[0] = [x.getFirst().id for x in line_list]
    lines[1] = [x.getLast().id for x in line_list]

    return lines


###############################################################################


def _get_slurs(part: music21.stream.Part) -> list[list[int]]:
    slurs: list[list[int]] = [[], []]
    slur_list = list(filter(_is_slur, part))
    slurs[0] = [x.getFirst().id for x in slur_list]
    slurs[1] = [x.getLast().id for x in slur_list]

    return slurs


###############################################################################


def _get_trems(part: music21.stream.Part) -> list[list[int]]:
    trems: list[list[int]] = [[], []]
    trem_list = list(filter(_is_trill, part))
    trems[0] = [x.getFirst().id for x in trem_list]
    trems[1] = [x.getLast().id for x in trem_list]

    return trems


###############################################################################


def _is_crescendo(elem: music21.Music21Object) -> bool:
    """
    Test to see if a music21 stream element is a crescendo or diminuendo
    object.

    Parameters
    ----------
    elem : music21.stream.Stream
        A music21 Stream element

    Return
    ------
    bool
        True iff `elem` is of type `music21.dynamics.Crescendo` or
        `music21.dynamics.Diminuendo`.
    """
    return isinstance(
        elem, (music21.dynamics.Crescendo, music21.dynamics.Diminuendo)
    )


###############################################################################


def _is_line(elem: music21.Music21Object) -> bool:
    """
    Test to see if a music21 stream element is a Line object.

    Parameters
    ----------
    elem : music21.stream.Stream
        A music21 Stream element

    Return
    ------
    bool
        True iff `elem` is of type `music21.spanner.Line`
    """
    return isinstance(elem, music21.spanner.Line)


###############################################################################


def _is_measure(elem: music21.Music21Object) -> bool:
    """
    Test to see if a music21 stream element is a Measure object.

    Parameters
    ----------
    elem : music21.stream.Stream
        A music21 Stream element

    Return
    ------
    bool
        True iff `elem` is of type `music21.stream.Measure`
    """
    return isinstance(elem, music21.stream.Measure)


###############################################################################


def _is_slur(elem: music21.Music21Object) -> bool:
    """
    Test to see if a music21 stream element is a Slur object.

    Parameters
    ----------
    elem : music21.stream.Stream
        A music21 Stream element

    Return
    ------
    bool
        True iff `elem` is of type `music21.spanner.Slur`
    """
    return isinstance(elem, music21.spanner.Slur)


###############################################################################


def _is_trill(elem: music21.Music21Object) -> bool:
    return isinstance(elem, music21.expressions.TrillExtension)


###############################################################################
# API class definitions
###############################################################################


class Song:
    """
    A complete song.

    Parameters
    ----------
    metadata: dict
        A dictionary containing the song's title (key "title"), composer (key
        "composer"), porter (key "porter") game name (key "game"), and global
        volume (key "volume").
    channels: list
        A list of `Channel` objects, the first 8 of which are used in this
        song.

    Attributes
    ----------
    title : str
        The song's title, or '???' if one was not provided
    composer : str
        The song's composer, or '???' if one was not provided
    porter : str
        The song's porter, or '???' if one was not provided
    game : str
        The song's source game, or '???' if one was not provided
    channels : list
        A list of up to 8 channels of music in this song.
    instruments: dict
        A dictionary of instrument name -> InstrumentConfig object for each
        detected instrument
    volume: int
        Global volume
    """

    ###########################################################################
    # API constructor definitions
    ###########################################################################

    def __init__(self, metadata: dict[str, str], channels: list["Channel"]):
        self.title = metadata.get("title", "???")
        self.composer = metadata.get("composer", "???")
        self.porter = metadata.get("porter", "???")
        self.game = metadata.get("game", "???")
        self.volume = int(metadata.get("volume", 180))
        self.channels = channels[:8]
        self.instruments: dict[str, InstrumentConfig] = {}

        self._reduced_channels: list["Channel"] = []

        self._collect_instruments()

    ###########################################################################

    @classmethod
    def from_music_xml(cls, fname: str) -> "Song":
        """
        Convert a MusicXML file to a Song.

        Parameters
        ----------
        fname : str
            The (compressed or uncompressed) MusicXML file

        Return
        ------
        Song
            A new Song object representing the song described in `fname`

        Raises
        ------
        MusicXmlException:
            Whenever a conversion is not possible
        """
        metadata = {}
        parts: list[Channel] = []

        try:
            stream = music21.converter.parseFile(fname)
        except music21.converter.ConverterFileException as e:
            raise MusicXmlException(str(e)) from e

        if not isinstance(stream, music21.stream.Score):
            raise MusicXmlException(
                f"Can only operate on Scores, not {type(stream)}s"
            )

        for elem in stream.flat:
            if isinstance(elem, music21.metadata.Metadata):
                metadata["composer"] = elem.composer or "COMPOSER HERE"
                metadata["title"] = elem.title or "TITLE HERE"
                metadata["porter"] = elem.lyricist or "PORTER NAME HERE"
                metadata["game"] = elem.copyright or "GAME NAME HERE"

        sections = cls._find_rehearsal_marks(stream)

        for elem in stream:
            if isinstance(elem, music21.stream.Part):
                part = cls._parse_part(elem, sections, len(parts))
                part = remove_unused_instruments(part)
                parts.append(Channel(part))

        return cls(metadata, parts)

    ###########################################################################
    # Data model method definitions
    ###########################################################################

    def __getitem__(self, n: int) -> Channel:
        return self.channels[n]

    ###########################################################################
    # Private method definitions
    ###########################################################################

    def _collect_instruments(self) -> None:
        inst_dyns: dict[str, set[Dynamics]] = {}
        transposes: dict[str, int] = {}

        for channel in self.channels:
            for token in channel.tokens:
                if isinstance(token, Instrument):
                    inst = token.name
                    if inst not in inst_dyns:
                        inst_dyns[inst] = set()
                        transposes[inst] = token.transpose
                if isinstance(token, Dynamic):
                    inst_dyns[inst].add(Dynamics[token.level.upper()])
                if isinstance(token, Crescendo):
                    inst_dyns[inst].add(Dynamics[token.target.upper()])

        inst_names = sorted(inst_dyns)

        self.instruments = {
            inst: InstrumentConfig.from_name(
                inst,
                dynamics_present=inst_dyns[inst],
                transpose=transposes[inst],
            )
            for inst in inst_names
        }

    ###########################################################################

    @classmethod
    def _find_rehearsal_marks(
        cls, stream: music21.stream.Score
    ) -> dict[int, RehearsalMark]:
        marks = {}
        for elem in stream:
            if isinstance(elem, music21.stream.Part):
                for measure in filter(_is_measure, elem):
                    for subelem in measure:
                        if isinstance(
                            subelem, music21.expressions.RehearsalMark
                        ):
                            marks[
                                measure.number
                            ] = RehearsalMark.from_music_xml(subelem)
                break
        return marks

    ###########################################################################

    @classmethod
    def _parse_part(
        cls,
        part: music21.stream.Part,
        sections: dict[int, RehearsalMark],
        part_no: int,
    ) -> list[Token]:
        channel_elem: list[Token] = []

        slurs = _get_slurs(part)
        trems = _get_trems(part)
        lines = _get_lines(part)
        loop_nos = list((part_no + 1) * 100 + n for n in range(len(lines[0])))
        cresc, cresc_type = _get_cresc(part)

        triplets = False
        for subpart in part:
            if isinstance(subpart, music21.instrument.Instrument):
                # This used to be .instrumentName, but that behaves...
                # unintuitively... on percussion channels
                name = subpart.partName or ""
                name = name.replace("\u266d", "b")  # Replace flats
                name = name.replace(" ", "")  # Replace spaces

                # Pick off the instrument transposition
                transpose = subpart.transposition
                semitones = transpose.semitones if transpose is not None else 0

                if not isinstance(semitones, int):
                    raise MusicXmlException(
                        f"Non-integer transposition {semitones}"
                    )

                semitones %= 12

                channel_elem.append(Instrument(name, semitones))
            if not isinstance(subpart, music21.stream.Measure):
                continue

            measure = subpart
            note_no = 0
            channel_elem.append(Measure(measure.number))
            if measure.number in sections:
                channel_elem.append(sections[measure.number])

            for subelem in measure:
                if subelem.id in lines[0]:
                    channel_elem.append(
                        LoopDelim(True, loop_nos[lines[0].index(subelem.id)])
                    )

                if isinstance(
                    subelem,
                    (music21.chord.Chord, music21.percussion.PercussionChord),
                ):
                    msg = f"Chord found, #{note_no + 1} "
                    msg += f"in measure {measure.number}"
                    channel_elem.append(Error(msg))

                if isinstance(subelem, (music21.stream.Voice)):
                    msg = f"Multiple voices in measure {measure.number}"
                    channel_elem.append(Error(msg))

                if isinstance(subelem, music21.note.GeneralNote):
                    note_no += 1
                    if not triplets and bool(subelem.duration.tuplets):
                        channel_elem.append(Triplet(True))
                        triplets = True

                    if triplets and not bool(subelem.duration.tuplets):
                        channel_elem.append(Triplet(False))
                        triplets = False

                if isinstance(subelem, music21.dynamics.Dynamic):
                    try:
                        channel_elem.append(Dynamic.from_music_xml(subelem))
                    except MusicXmlException as e:
                        msg = f"{e} in measure {measure.number}"
                        channel_elem.append(Error(msg))
                if isinstance(
                    subelem, (music21.note.Note, music21.note.Unpitched)
                ):
                    note = Note.from_music_xml(subelem)
                    if subelem.id in slurs[0]:
                        channel_elem.append(Slur(True))
                    # It seems weird to put slur-ends before the actual last
                    # slur note.  But the note that comes at the slur-end needs
                    # to know it so the legato can be put in the right place.
                    if subelem.id in slurs[1]:
                        channel_elem.append(Slur(False))

                    # Gross, fix this
                    subelem_id = subelem.id
                    if not isinstance(subelem_id, int):
                        raise MusicXmlException(
                            f"Non-integer element ID {subelem_id}"
                        )

                    if subelem_id in cresc[0]:
                        channel_elem.append(
                            CrescDelim(
                                True, cresc_type[cresc[0].index(subelem_id)]
                            )
                        )

                    if subelem.id in trems[0]:
                        channel_elem.append(Vibrato(True))

                    note.measure_num = measure.number
                    note.note_num = note_no
                    channel_elem.append(note)

                    if subelem.id in trems[1]:
                        channel_elem.append(Vibrato(False))

                    # Also gross, fix this
                    subelem_id = subelem.id
                    if not isinstance(subelem_id, int):
                        raise MusicXmlException(
                            f"Non-integer element ID {subelem_id}"
                        )

                    if subelem_id in cresc[1]:
                        channel_elem.append(
                            CrescDelim(
                                False, cresc_type[cresc[1].index(subelem_id)]
                            )
                        )

                if isinstance(subelem, music21.bar.Repeat):
                    channel_elem.append(Repeat.from_music_xml(subelem))
                if isinstance(subelem, music21.note.Rest):
                    rest = Rest.from_music_xml(subelem)
                    rest.measure_num = measure.number
                    rest.note_num = note_no
                    channel_elem.append(rest)
                if isinstance(subelem, music21.expressions.TextExpression):
                    annotation = Annotation.from_music_xml(subelem)
                    if annotation is not None:
                        channel_elem.append(annotation)
                if isinstance(subelem, music21.tempo.MetronomeMark):
                    channel_elem.append(Tempo.from_music_xml(subelem))
                if isinstance(subelem, music21.clef.Clef):
                    channel_elem.append(Clef.from_music_xml(subelem))

                if subelem.id in lines[1]:
                    channel_elem.append(
                        LoopDelim(False, loop_nos[lines[1].index(subelem.id)])
                    )
        if triplets:
            channel_elem.append(Triplet(False))

        return channel_elem

    ###########################################################################

    def _reduce(
        self,
        loop_analysis: bool,
        superloop_analysis: bool,
    ) -> None:
        self._reduced_channels = copy.deepcopy(self.channels)

        for n, chan in enumerate(self._reduced_channels):
            chan.tokens = reduce(
                chan.tokens,
                loop_analysis,
                superloop_analysis,
                n != 0,
            )

    ###########################################################################

    def _validate(self) -> None:
        errors = []
        for n, channel in enumerate(self._reduced_channels):
            msgs = channel.check(self.instruments)
            for msg in msgs:
                errors.append(f"{msg} in staff {n + 1}")

        if errors:
            raise MusicXmlException("\n".join(errors))

    ###########################################################################
    # API method definitions
    ###########################################################################

    def generate_mml(
        self,
        global_legato: bool = True,
        loop_analysis: bool = True,
        superloop_analysis: bool = True,
        measure_numbers: bool = True,
        include_dt: bool = True,
        echo_config: EchoConfig | None = None,
        sample_path: PurePosixPath | None = None,
        start_measure: int = 1,
    ) -> str:
        """
        Return this song's AddmusicK's text.

        Parameters
        ----------
        global_legato : bool
            True iff global legato should be enabled
        loop_analysis : bool
            True iff loops should be detected and replaced with references
        superloop_analysis: bool
            True iff loops should be detected
        measure_numbers: bool
            True iff measure numbers should be included in MML
        include_dt: bool
            True iff current date/time is included in MML
        echo_config: EchoConfig
            Echo configuration
        sample_path: PurePosicPath
            Base path where custom BRR samples are stored
        start_measure: int
            First measure of music to output
        """

        # If starting after the first measure, disable loop analysis because
        # things might be badly broken
        if start_measure != 1:
            loop_analysis = False
            superloop_analysis = False

        self._reduce(loop_analysis, superloop_analysis)

        # TODO: A bit of a hack to allow starting at a later measure
        if start_measure != 1:
            for channel in self._reduced_channels:
                to_drop = start_measure - 1
                tokens: list[Token] = []
                for n, token in enumerate(channel.tokens):
                    if isinstance(
                        token, (Dynamic, Instrument, Measure, Tempo, Repeat)
                    ):
                        tokens.append(token)
                        if isinstance(token, Measure):
                            to_drop -= 1
                    if to_drop == 0:
                        tokens.extend(channel.tokens[n + 1 :])
                        break
                channel.tokens = tokens

        self._validate()
        channels = [
            x.generate_mml(self.instruments, measure_numbers)
            for x in self._reduced_channels
        ]

        build_dt = ""
        if include_dt:
            build_dt = datetime.utcnow().isoformat(" ", "seconds") + " UTC"

        instruments = copy.deepcopy(self.instruments)
        inst_samples: dict[str, InstrumentSample] = {}

        for inst_name, inst in instruments.items():
            if inst.multisample:
                inst_samples.update(inst.multisamples)
            else:
                inst_samples[inst_name] = inst.samples[""]

        samples: list[tuple[str, str, int]] = []
        sample_id = 30

        for sample in inst_samples.values():
            if sample.sample_source == SampleSource.SAMPLEPACK:
                fname = str(
                    PurePosixPath(sample.pack_sample[0])
                    / sample.pack_sample[1]
                )
                samples.append((fname, sample.brr_str, sample_id))
                sample.instrument_idx = sample_id
                sample_id += 1
            if sample.sample_source == SampleSource.BRR:
                fname = sample.brr_fname.name
                samples.append((fname, sample.brr_str, sample_id))
                sample.instrument_idx = sample_id
                sample_id += 1

        # Overwrite muted/soloed instrument sample numbers
        solo = any(sample.solo for sample in inst_samples.values())
        mute = any(sample.mute for sample in inst_samples.values())
        solo |= any(inst.solo for inst in instruments.values())
        mute |= any(inst.mute for inst in instruments.values())

        if solo or mute:
            samples.append(("../EMPTY.brr", "$00 $00 $00 $00 $00", sample_id))

            for inst_sample in inst_samples.values():
                if inst_sample.mute or (solo and not inst_sample.solo):
                    inst_sample.sample_source = SampleSource.OVERRIDE
                    inst_sample.instrument_idx = sample_id

            # Not necessary, but we keep it for consistency's sake
            sample_id += 1

        tmpl = Template(  # nosec B702
            pkgutil.get_data("smw_music", "data/mml.txt")
        )

        rv = tmpl.render(
            version=__version__,
            global_legato=global_legato,
            song=self,
            channels=channels,
            datetime=build_dt,
            echo_config=echo_config,
            inst_samples=inst_samples,
            custom_samples=samples,
            dynamics=list(Dynamics),
            sample_path=str(sample_path),
        )

        rv = rv.replace(" ^", "^")
        rv = rv.replace(" ]", "]")

        # This last bit removes any empty lines at the end (these don't
        # normally show up, but can if the last section in the last staff is
        # empty.
        return str(rv).rstrip() + CRLF

    ###########################################################################

    def to_mml_file(  # pylint: disable=too-many-arguments
        self,
        fname: str,
        global_legato: bool = True,
        loop_analysis: bool = True,
        superloop_analysis: bool = True,
        measure_numbers: bool = True,
        include_dt: bool = True,
        echo_config: EchoConfig | None = None,
        sample_path: PurePosixPath | None = None,
        start_measure: int = 1,
    ) -> str:
        """
        Output the MML representation of this Song to a file.

        Parameters
        ----------
        fname : str
            The output file to write to.
        global_legato : bool
            True iff global legato should be enabled
        loop_analysis: bool
            True iff loops should be detected and replaced with references
        superloop_analysis: bool
            True iff loops should be detected
        measure_numbers: bool
            True iff measure numbers should be included in MML
        include_dt: bool
            True iff current date/time is included in MML
        echo_config: EchoConfig
            Echo configuration
        sample_path: PurePosicPath
            Base path where custom BRR samples are stored
        start_measure: int
            First measure of music to output
        """
        mml = self.generate_mml(
            global_legato,
            loop_analysis,
            superloop_analysis,
            measure_numbers,
            include_dt,
            echo_config,
            sample_path,
            start_measure,
        )

        if fname:
            with open(fname, "wb") as fobj:
                fobj.write(mml.encode("ascii", "ignore"))

        return mml

    ###########################################################################

    def unmapped_notes(
        self, inst_name: str, inst: InstrumentConfig
    ) -> list[tuple[music21.pitch.Pitch, NoteHead]]:
        rv = list()

        instrument = inst if inst.multisample else None
        for channel in self.channels:
            rv.extend(channel.unmapped(inst_name, instrument))

        return dedupe_notes(rv)

    ###########################################################################
    # API property definitions
    ###########################################################################

    @property
    def rehearsal_marks(self) -> dict[str, int]:
        """A dictionary mapping rehearsal marks to measure numbers"""

        rv: dict[str, int] = {}
        for token in self.channels[0]:
            if isinstance(token, Measure):
                measure = token.range[0]
            if isinstance(token, RehearsalMark):
                rv[token.mark] = measure

        return rv
