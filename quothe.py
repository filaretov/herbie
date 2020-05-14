import numpy as np
import scipy as sp
from typing import List, Tuple, Callable
from notes import note_freq

class Generator:
    def __init__(self, fn: Callable = np.sin, rate: int = 44100):
        self.rate = rate
        self.fn = fn
        self.filters = []

    def signal(self, frequency: float, fn: Callable = None, duration: float = 1):
        fn = fn or self.fn
        n = int(duration * self.rate)
        t = np.linspace(0, 1 * duration, int(self.rate * duration))
        s = fn(t * 2 * np.pi * frequency)
        for f in self.filters:
            s = f(s)
        return s

    def chord(self, notes: List[str], fn: Callable = None, duration: float = 1):
        fn = fn or self.fn
        signals = []
        for n in notes:
            signals.append(self.signal(note_freq[n], fn, duration=duration))
        return np.sum(signals, axis=0)

    def melody(self, notes: List[Tuple[str, float]], fn: Callable = None) -> np.array:
        """The notes should be a list of tuples: [("A4", 1/2), ("B4", 1/4)].
        If only a single note (str) is found, it is converted to (str, 1)."""
        fn = fn or self.fn
        fill_duration = lambda n: (n, 1) if type(n) == str else n
        change_to_chord = lambda n: ([n[0]], n[1]) if type(n[0]) == str else n
        notes = [fill_duration(n) for n in notes]
        notes = [change_to_chord(n) for n in notes]
        melody = np.concatenate([self.chord(n, duration=d) for n, d in notes])
        return melody

