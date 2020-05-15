import numpy as np
from typing import Tuple, List


def clip(a: np.array, threshold: float, mix: float = 1) -> np.array:
    max = np.max(a)
    if max == 0:
        # a is a zero array
        return a
    c = a / max
    c = np.where(a < threshold, a, threshold)
    c = np.where(c > -threshold, c, -threshold)
    c = c * max
    return mix * c + (1 - mix) * a


def normalize(a: np.array) -> np.array:
    max = np.max(a)
    if max == 0:
        return a
    return a / np.max(a)


def adsr(
    s: np.array,
    attack: Tuple[float, float],
    decay: Tuple[float, float],
    release: Tuple[float, float],
    mix: float = 1,
) -> np.array:
    """This isn't reeeeally an ADSR filter, but it's inspired by it."""
    length = len(s)
    (att_l, att_n) = (attack[0], int(length * attack[1]))
    (dec_l, dec_n) = (decay[0], int(length * decay[1]))
    (rel_l, rel_n) = (release[0], int(length * release[1]))
    sus_n = length - (att_n + dec_n + rel_n)

    att = np.linspace(0, att_l, att_n)
    dec = np.linspace(att_l, dec_l, dec_n)
    sus = np.linspace(dec_l, dec_l, sus_n)
    rel = np.linspace(dec_l, rel_l, rel_n)

    adsr = np.concatenate([att, dec, sus, rel])
    assert len(adsr) == length

    f = np.multiply(s, adsr)
    return mix * f + (1 - mix) * s

def masher(parts: List[np.array]) -> np.array:
    mlen = np.max([len(p) for p in parts])
    padded = []
    for p in parts:
        padded.append(np.pad(p, (0, mlen - len(p))))
    mashed = np.sum(padded, axis=0)
    return filters.normalize(mashed)

def pad(parts: List[np.array]) -> np.array:
    mlen = np.max([len(p) for p in parts])
    padded = []
    for p in parts:
        padded.append(np.pad(p, (0, mlen - len(p))))
    return padded
