import numpy as np


def generate_time(duration, rate):
    samples = int(duration * rate)
    return np.linspace(0, duration, samples, False)

def generate_sine(time, amplitude, frequency, phase):
    sineArr = amplitude*np.sin(np.pi * 2 * frequency * time + phase)
    return sineArr



