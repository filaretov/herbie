import numpy as np
import scipy as sp
from typing import List, Tuple, Callable
from notes import note_freq

class Generator:
    def __init__(self, fn: Callable = np.sin, rate: int = 44100):
        self.rate = rate
        self.fn = fn
        self.attack = (1, 1/32)
        self.decay = (3/4, 1/8)
        self.release = (0, 1/64)

    def signal(self, frequency: float, fn: Callable = None, duration: float = 1):
        fn = fn or self.fn
        n = int(duration * self.rate)
        t = np.linspace(0, 1 * duration, int(self.rate * duration))
        s = fn(t * 2 * np.pi * frequency)
        filter = self._adsr(n, attack=self.attack, decay=self.decay, release=self.release)
        filtered = np.multiply(s, filter)
        return filtered

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

    def _trapezoid(self, length: int):
        slope = int(length / 16)
        rise = np.linspace(0, 1, slope)
        flat = np.ones(length - 2 * slope)
        fall = np.linspace(1, 0, slope)
        return np.concatenate([rise, flat, fall])

    def _adsr(
            self, length: int, attack: Tuple[float, float], decay: Tuple[float, float], release: Tuple[float, float]
    ):
        """This isn't reeeeally an ADSR filter, but it's inspired by it."""
        (att_l, att_n) = (attack[0], int(length*attack[1]))
        (dec_l, dec_n) = (decay[0], int(length*decay[1]))
        (rel_l, rel_n) = (release[0], int(length*release[1]))
        sus_n = length - (att_n + dec_n + rel_n)

        att = np.linspace(0, att_l, att_n)
        dec = np.linspace(att_l, dec_l, dec_n)
        sus = np.linspace(dec_l, dec_l, sus_n)
        rel = np.linspace(dec_l, rel_l, rel_n)

        adsr = np.concatenate([att, dec, sus, rel])
        assert len(adsr) == length
        return adsr

