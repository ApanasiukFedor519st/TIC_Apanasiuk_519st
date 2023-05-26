import os
from math import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt
import scipy
from random import randint


def main(frequency_ask, frequency_psk, frequency_fsk1, frequency_fsk2):
    sequence = create_sequence()
    x = np.arange(len(sequence)) / 1000
    plot(x, sequence, "Time, s", "Signal Amplitude", "Random Sequence")

    sequence_ask = ask_modulation(frequency_ask, sequence)
    plot(x, sequence_ask, "Time, s", "Signal Amplitude", "Amplitude Modulation")
    x_spectrum, spectrum_sequence_ask = spectrum(sequence_ask)
    plot(x_spectrum, spectrum_sequence_ask, "Frequency, Hz", "Spectrum Amplitude", "Spectrum of Amplitude Modulation")

    sequence_psk = psk_modulation(frequency_psk, sequence)
    plot(x, sequence_psk, "Time, s", "Signal Amplitude", "Phase Modulation")
    x_spectrum, spectrum_sequence_psk = spectrum(sequence_psk)
    plot(x_spectrum, spectrum_sequence_psk, "Frequency, Hz", "Spectrum Amplitude", "Spectrum of Phase Modulation")

    sequence_fsk = fsk_modulation(frequency_fsk1, frequency_fsk2, sequence)
    plot(x, sequence_fsk, "Time, s", "Signal Amplitude", "Frequency Modulation")
    x_spectrum, spectrum_sequence_fsk = spectrum(sequence_fsk)
    plot(x_spectrum, spectrum_sequence_fsk, "Frequency, Hz", "Spectrum Amplitude", "Spectrum of Frequency Modulation")

    noise = create_noise(0, 1, 1000)
    sequence_ask_noise = sequence_ask + noise
    sequence_psk_noise = sequence_psk + noise
    sequence_fsk_noise = sequence_fsk + noise

    plot(x, sequence_ask_noise, "Time, s", "Signal Amplitude", "Amplitude Modulation with Noise")
    plot(x, sequence_psk_noise, "Time, s", "Signal Amplitude", "Phase Modulation with Noise")
    plot(x, sequence_fsk_noise, "Time, s", "Signal Amplitude", "Frequency Modulation with Noise")

    ask_demodulated_signal, sequence_demodulated = ask_demodulation(frequency_ask, sequence_ask_noise)
    plot(x, ask_demodulated_signal, "Time, s", "Signal Amplitude", "Demodulated Signal (Amplitude Modulation)")
    plot(x, sequence_demodulated, "Time, s", "Signal Amplitude", "Demodulated Sequence (Amplitude Modulation)")

    psk_demodulated_signal, sequence_demodulated = psk_demodulation(frequency_psk, sequence_psk_noise)
    plot(x, psk_demodulated_signal, "Time, s", "Signal Amplitude", "Demodulated Signal (Phase Modulation)")
    plot(x, sequence_demodulated, "Time, s", "Signal Amplitude", "Demodulated Sequence (Phase Modulation)")

    fsk_demodulated_signal1, fsk_demodulated_signal2, sequence_demodulated = fsk_demodulation(frequency_fsk1,
                                                                                              frequency_fsk2,
                                                                                              sequence_fsk_noise)
    plot(x, fsk_demodulated_signal1, "Time, s", "Signal Amplitude", "Demodulated Signal 1 (Frequency Modulation)")
    plot(x, fsk_demodulated_signal2, "Time, s", "Signal Amplitude", "Demodulated Signal 2 (Frequency Modulation)")
    plot(x, sequence_demodulated, "Time, s", "Signal Amplitude", "Demodulated Sequence (Frequency Modulation)")


def create_sequence():
    sequence = np.zeros(1000)
    sequence[0:100] = randint(0, 1)
    sequence[100:200] = randint(0, 1)
    sequence[200:300] = randint(0, 1)
    sequence[300:400] = randint(0, 1)
    sequence[400:500] = randint(0, 1)
    sequence[500:600] = randint(0, 1)
    sequence[600:700] = randint(0, 1)
    sequence[700:800] = randint(0, 1)
    sequence[800:900] = randint(0, 1)
    sequence[900:999] = randint(0, 1)
    return sequence


def create_noise(mean, standard_deviation, length):
    return np.random.normal(mean, standard_deviation, length)


def ask_modulation(frequency, sequence):
    return sequence * sin(2 * pi * frequency * np.arange(len(sequence)) / 1000)


def psk_modulation(frequency, sequence):
    return sequence * cos(2 * pi * frequency * np.arange(len(sequence)) / 1000)


def fsk_modulation(frequency1, frequency2, sequence):
    modulated_signal = np.zeros(len(sequence))
    for i in range(len(sequence)):
        if sequence[i] == 0:
            modulated_signal[i] = sin(2 * pi * frequency1 * i / 1000)
        else:
            modulated_signal[i] = sin(2 * pi * frequency2 * i / 1000)
    return modulated_signal


def ask_demodulation(frequency, signal):
    demodulated_signal = signal * sin(2 * pi * frequency * np.arange(len(signal)) / 1000)
    demodulated_sequence = np.zeros(len(demodulated_signal))
    for i in range(len(demodulated_signal)):
        if demodulated_signal[i] > 0:
            demodulated_sequence[i] = 1
    return demodulated_signal, demodulated_sequence


def psk_demodulation(frequency, signal):
    demodulated_signal = signal * cos(2 * pi * frequency * np.arange(len(signal)) / 1000)
    demodulated_sequence = np.zeros(len(demodulated_signal))
    for i in range(len(demodulated_signal)):
        if demodulated_signal[i] > 0:
            demodulated_sequence[i] = 1
    return demodulated_signal, demodulated_sequence


def fsk_demodulation(frequency1, frequency2, signal):
    demodulated_signal1 = signal * sin(2 * pi * frequency1 * np.arange(len(signal)) / 1000)
    demodulated_signal2 = signal * sin(2 * pi * frequency2 * np.arange(len(signal)) / 1000)
    demodulated_sequence = np.zeros(len(signal))
    for i in range(len(signal)):
        if abs(demodulated_signal1[i]) > abs(demodulated_signal2[i]):
            demodulated_sequence[i] = 0
        else:
            demodulated_sequence[i] = 1
    return demodulated_signal1, demodulated_signal2, demodulated_sequence


def spectrum(signal):
    spectrum = np.fft.fft(signal)
    x_spectrum = np.fft.fftfreq(len(spectrum))
    return x_spectrum, abs(spectrum)


def plot(x, y, xlabel, ylabel, title):
    plt.figure()
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


main(40, 40, 60, 30)
