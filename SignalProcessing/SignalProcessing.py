from scipy import signal, fft
import numpy
import scipy
import matplotlib.pyplot as plt

n = 500
Fs = 1000
Fmax = 5

random = numpy.random.normal(0, 10, n)
time_line_ox = numpy.arange(n)/Fs

w = Fmax/(Fs/2)

parameters_filter = scipy.signal.butter(3, w, 'low', output='sos')

filtered_signal = scipy.signal.sosfiltfilt(parameters_filter, random)

fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(time_line_ox, filtered_signal, linewidth = 1)
ax.set_xlabel("Час (секунди) ", fontsize = 14)
ax.set_ylabel("Амплітуда сигналу ", fontsize = 14)
plt.title("Сигнал з максимальною частотой Fmax = 5", fontsize = 14)
ax.grid()
fig.savefig('./figures/' + 'графік 1' + '.png', dpi = 600)
dpi = 600

spectrum = scipy.fft.fft(filtered_signal)
spectrum = numpy.abs(scipy.fft.fftshift(spectrum))
length_signal = n
freq_countdown = scipy.fft.fftfreq(length_signal, 1/length_signal)
freq_countdown = scipy.fft.fftshift(freq_countdown)

fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(freq_countdown, spectrum, linewidth = 1)
ax.set_xlabel("Частота (Гц)", fontsize = 14)
ax.set_ylabel("Амплітуда спектра ", fontsize = 14)

plt.title("Спектр сигнала с максимальной частотой Fmax = 5", fontsize = 14)
ax.grid()
fig.savefig('./figures/' + 'графік 2' + '.png', dpi=600)