import numpy as np
from typing import Tuple

modes = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "chromatic": list(range(0, 12)),
}


class Scale:
    def __init__(self, root: str = "C", mode: str = "major", octave: int = 4):
        self.mode = mode
        self.root = root_index[root] + (octave * 12)
        self.intervals = modes[mode]
        self.scale_length = len(self.intervals)
        assert 0 <= octave <= 8
        self.octave = octave

    def note(self, note: int, octave: int = None):
        octave = octave or self.octave
        return self.notes[octave, note]

    def chord(self, root: int, octave_shift: int = 0) -> Tuple:
        root = self[octave_shift, interval]
        third = self[octave_shift, interval+2]
        fifth = self[octave_shift, interval+4]
        seventh = self[octave_shift, interval+6]
        return np.array((root, third, fifth, seventh))

    def __getitem__(self, index):
        if type(index) == tuple:
            octave, interval = index
        elif type(index) == int:
            octave, interval = 0, index
        add_octave, interval = divmod(interval, self.scale_length)
        octave += add_octave
        print(f"{octave=}, {interval=}")
        return _all_notes[self.root + self.intervals[interval] + (octave * 12)]


class Note:
    pass


class Chord:
    def __getitem__(self, arg):
        return 0


noctaves = 9
nsemitones = 12
_all_notes = np.array(
    [
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
)


root_index = {
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
