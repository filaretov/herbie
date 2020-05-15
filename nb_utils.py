import librosa
import numpy as np
import IPython.display as ipd

from herbie.filters import normalize


def play(a: np.array, rate: int = 44100, volume: float = 0.2, repeat: int = 1, autoplay=True):
    wave = np.tile(a, repeat)
    return ipd.Audio(wave, rate=rate, autoplay=autoplay)

def to_wav(filename: str, a: np.array, rate: int = 44100):
    librosa.output.write_wav(filename, normalize(a), rate)
