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

F_filter = 12
dispersions = []
signal_noise = []
discrete_spectrums = []
E1 = []
discrete_signals = []
discrete_signal_after_filers = []
w = F_filter / (Fs / 2)
parameters_fil = scipy.signal.butter(3, w, 'low', output='sos')
filtered_signal_2 = None
for Dt in [2, 4, 8, 16]:
    discrete_signal = numpy.zeros(n)
    for i in range(0, round(n / Dt)):
        discrete_signal[i * Dt] = filtered_signal[i * Dt]
        filtered_signal_2 = scipy.signal.sosfiltfilt(parameters_fil, discrete_signal)
    discrete_signals += [list(discrete_signal)]
    discrete_spectrum = scipy.fft.fft(discrete_signals)
    discrete_spectrum = numpy.abs(scipy.fft.fftshift(discrete_spectrum))
    discrete_spectrums.append(list(discrete_spectrum))
    discrete_signal_after_filers += [list(filtered_signal_2)]

for i in range(4):
    E1 = discrete_signal_after_filers[i] - filtered_signal
    dispersion = numpy.var(E1)
    dispersions.append(dispersion)
    signal_noise.append(numpy.var(filtered_signal)/dispersion)

fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(time_line_ox, discrete_signals[s], linewidth=1)
        ax[i][j].grid()
        s += 1
fig.supxlabel('Час (секунди)', fontsize=14)
fig.supylabel('Амплітуда сигналу', fontsize=14)
fig.suptitle('Сигнал з кроком дискретизації Dt = (2,4,8,16)', fontsize=14)
fig.savefig('./figures/' + 'графік 3' + '.png', dpi=600)

s = 0
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(freq_countdown, discrete_spectrum[s], linewidth=1)
        s += 1
fig.supxlabel("Частота (Гц)", fontsize=14)
fig.supylabel("Амплитуда спектра", fontsize=14)
fig.suptitle("Сигнал з шагом дискретизации Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig('./figures/' + 'график 4' + '.png', dpi=600)

fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(time_line_ox, discrete_signal_after_filers[s], linewidth=1)
        ax[i][j].grid()
        s += 1
fig.supxlabel('Час (секунди)', fontsize=14)
fig.supylabel('Амплітуда сигналу', fontsize=14)
fig.suptitle('Відновлені аналогові сигнали з кроком дискретизації Dt = (2,4,8,16)', fontsize=14)
fig.savefig('./figures/' + 'графік 5' + '.png', dpi=600)

fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot((2,4,8,16), dispersions, linewidth=1)
ax.set_xlabel('Крок дискретизації', fontsize=14)
ax.set_ylabel('Дисперсія', fontsize=14)
plt.title(f'Залежність дисперсії від кроку дискретизації', fontsize=14)
ax.grid()
fig.savefig('./figures/' + 'графік 6' + '.png', dpi=600)

fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot((2,4,8,16), signal_noise, linewidth=1)
ax.set_xlabel('Крок дискретизації', fontsize=14)
ax.set_ylabel('ССШ', fontsize=14)
plt.title(f'Залежність співвідношення сигнал-шум від кроку дискретизації', fontsize=14)
ax.grid()
fig.savefig('./figures/' + 'графік 7' + '.png', dpi=600)

