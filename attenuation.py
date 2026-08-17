import numpy as np

def attenuate(signal, time, fadingfrequency):
    fading = 0.25 * np.sin(2 * np.pi * fadingfrequency * time) + 0.75       # Fading ranges from 0.5 to 1
    signal = signal * fading
    return signal