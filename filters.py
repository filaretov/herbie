import numpy as np

def clip(a: np.array, threshold: float, both: bool = True) -> np.array:
    max = np.max(a)
    a = a / max
    a = np.where(a < threshold, a, threshold)
    if both:
        a = np.where(a > -threshold, a, -threshold)
    clipped = a * max
    return clipped


def normalize(a: np.array) -> np.array:
    return a / np.max(a)
