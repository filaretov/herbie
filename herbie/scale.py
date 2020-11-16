from typing import Tuple, List
from parse import parse

from .notes import frequencies

modes = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "chromatic": list(range(0, 12)),
}

all_notes = "CDEFGAB"


class Scale:
    def __init__(self, root: str = "C", mode: str = "major", octave: int = 4, bpm: float = 120, beat_note: int = 4, default_note: int = 4):
        beat_note_duration = (60 / bpm)
        self.whole_note_duration = beat_note_duration * beat_note
        self.default_note = default_note
        self.mode = mode
        self.octave = octave
        self.root = root
        self.bpm = bpm
        self.intervals = modes[mode]
        self.scale_length = len(self.intervals)

        note_index = all_notes.find(root)
        self.notes = all_notes[note_index:] + all_notes[:note_index]
        self.note_index = {note: index for index, note in enumerate(self.notes)}

    @property
    def root_index(self):
        return ROOT_INDEX[self.root] + (self.octave * 12)

    def note_from_root(self, note_name: str, octave: int = 0) -> float:
        if note_name == "r":
            return 0
        interval = self.note_index[note_name]
        add_octave, interval = divmod(interval, self.scale_length)
        octave += add_octave
        return note_frequencies[
            self.root_index + self.intervals[interval] + (octave * 12)
        ]

    def sequence(self, seq: str) -> List:
        note_tokens = seq.strip().split(" ")
        note_sequence = []
        for token in note_tokens:
            notelets, duration = self.parse_note_token(token)
            frequencies = [
                self.note_from_root(note_name, octave_shift)
                for note_name, octave_shift in notelets
            ]
            duration = self.whole_note_duration / duration
            note_sequence.append((frequencies, duration))
        return note_sequence

    def parse_note_token(self, token: str) -> Tuple[str, int]:
        if r := parse("{note_spec}.{duration}", token):
            note_spec = r["note_spec"]
            duration = float(r["duration"])
        elif r := parse("{note_spec}", token):
            note_spec = r["note_spec"]
            duration = float(self.default_note)
        else:
            raise InvalidNoteTokenException(f"'{token}' is not a valid token.")
        notelets = self.parse_note_spec_token(note_spec)
        return (notelets, duration)

    def parse_note_spec_token(self, token: str) -> List[Tuple[str, int]]:
        notelet_tokens = token.split("-")
        return [self.parse_notelet_token(token) for token in notelet_tokens]

    def parse_notelet_token(self, token: str) -> Tuple[str, int]:
        if r := parse("{note}^", token):
            note = r["note"]
            octave_shift = 1
        elif r := parse("{note}v", token):
            note = r["note"]
            octave_shift = -1
        else:
            note = token
            octave_shift = 0
        return note, octave_shift

    def chord(self, root: int, octave_shift: int = 0) -> Tuple:
        unison = self[octave_shift, root]
        third = self[octave_shift, root + 2]
        fifth = self[octave_shift, root + 4]
        seventh = self[octave_shift, root + 6]
        return (unison, third, fifth, seventh)

    def __getitem__(self, interval):
        add_octave, interval = divmod(interval, self.scale_length)
        octave += add_octave
        return note_frequencies[
            self.root_index + self.intervals[interval] + (octave * 12)
        ]

    def __str__(self) -> str:
        return f"Scale: {self.root} {self.mode}"

    def __repr__(self) -> str:
        return str(self.__dict__)


class Note:
    pass


class Chord:
    def __getitem__(self, arg):
        return 0


noctaves = 9
nsemitones = 12
note_frequencies = [
    16.35,
    17.32,
    18.35,
    19.45,
    20.60,
    21.83,
    23.12,
    24.50,
    25.96,
    27.50,
    29.14,
    30.87,
    32.70,
    34.65,
    36.71,
    38.89,
    41.20,
    43.65,
    46.25,
    49.00,
    51.91,
    55.00,
    58.27,
    61.74,
    65.41,
    69.30,
    73.42,
    77.78,
    82.41,
    87.31,
    92.50,
    98.00,
    103.83,
    110.00,
    116.54,
    123.47,
    130.81,
    138.59,
    146.83,
    155.56,
    164.81,
    174.61,
    185.00,
    196.00,
    207.65,
    220.00,
    233.08,
    246.94,
    261.63,
    277.18,
    293.66,
    311.13,
    329.63,
    349.23,
    369.99,
    392.00,
    415.30,
    440.00,
    466.16,
    493.88,
    523.25,
    554.37,
    587.33,
    622.25,
    659.25,
    698.46,
    739.99,
    783.99,
    830.61,
    880.00,
    932.33,
    987.77,
    1046.50,
    1108.73,
    1174.66,
    1244.51,
    1318.51,
    1396.91,
    1479.98,
    1567.98,
    1661.22,
    1760.00,
    1864.66,
    1975.53,
    2093.00,
    2217.46,
    2349.32,
    2489.02,
    2637.02,
    2793.83,
    2959.96,
    3135.96,
    3322.44,
    3520.00,
    3729.31,
    3951.07,
    4186.01,
    4434.92,
    4698.63,
    4978.03,
    5274.04,
    5587.65,
    5919.91,
    6271.93,
    6644.88,
    7040.00,
    7458.62,
    7902.13,
]


ROOT_INDEX = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}


class InvalidNoteTokenException(Exception):
    pass
