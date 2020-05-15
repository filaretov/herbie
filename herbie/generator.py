import numpy as np
import scipy as sp
from typing import List, Tuple, Callable

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

    def chord(self, notes: List[float], fn: Callable = None, duration: float = 1):
        fn = fn or self.fn
        signals = []
        for n in notes:
            signals.append(self.signal(n, fn, duration=duration))
        return np.sum(signals, axis=0)

    def sequence(self, notes: List[Tuple[float, float]], fn: Callable = None) -> np.ndarray:
        """The notes should be a list of tuples: [(440, 1/2), (880, 1/4)].
        The first element can also be a tuple: [((440, 880), 1/2), (880, 1/4)].
        If only a single note (float) is found, it is converted to (float, 1)."""
        fn = fn or self.fn
        fill_duration = lambda n: n if isinstance(n, (tuple, list, np.ndarray)) else (n, 1)
        change_to_chord = lambda n: n if isinstance(n[0], (tuple, list, np.ndarray)) else ((n[0],), n[1])
        notes = [fill_duration(n) for n in notes]
        notes = [change_to_chord(n) for n in notes]
        melody = np.concatenate([self.chord(n, duration=d) for n, d in notes])
        return melody

