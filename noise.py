import numpy as np

def add_noise(signal, stdev):
    noiseArr = np.random.normal(0, stdev, len(signal))
    return noiseArr + signal, noiseArr