#!/usr/bin/env python

"""
Frequency shift a signal using SSB modulation.
"""

import numpy as np
import scipy as sp
import scipy.signal
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt



def nextpow2(x):
    """Return the first integer N such that 2**N >= abs(x)"""

    return int(np.ceil(np.log2(np.abs(x))))

def freq_shift(x, f_shift, dt):
    """
    Shift the specified signal by the specified frequency.
    """

    # Pad the signal with zeros to prevent the FFT invoked by the transform from
    # slowing down the computation:
    N_orig = len(x)
    N_padded = 2**nextpow2(N_orig)
    t = np.arange(0, N_padded)
    return (scipy.signal.hilbert(np.hstack((x, np.zeros(N_padded-N_orig, x.dtype))))*np.exp(2j*np.pi*f_shift*dt*t))[:N_orig].real

dt = 1e-3 #Fraction of a millisecond
fs = int(1/dt)
#T = 1.0
#t = np.linspace(-1, 1, 2 *(1/dt), endpoint=False) #np.arange(0, T, dt)


# Construct original signal:
#x = 3*np.cos(2*np.pi*t)+np.cos(2*np.pi*3*t)+2*np.cos(2*np.pi*5*t)
#x = scipy.signal.gausspulse(t, fc=5)

#Resolution is given in nanoseconds
#PulsePeriod is given in milliseconds

def GaussPulseTrain(PulseNum, Res, PulsePeriod ,RadioFreq, FracBandWidth):
    tInit = np.linspace(-PulsePeriod*1e-3/2, PulsePeriod*1e-3/2, 2 * Res, endpoint=False)
    SeedSignal = sp.signal.gausspulse(tInit, fc=RadioFreq, bw=FracBandWidth)
    signalArray = []
    signalTime = []
    s = []
    for x in range(0, PulseNum):
        signalArray = np.append(signalArray,SeedSignal)
        s = np.linspace(-PulsePeriod*1e-3/2 + 2*PulsePeriod*1e-3/2*x, PulsePeriod*1e-3/2 + 2*PulsePeriod*1e-3/2*x, 2 * Res, endpoint=False)
        signalTime = np.append(signalTime, s)
    return signalTime, signalArray

def GaussPulseTrainNoise(PulseNum, Res, PulsePeriod ,RadioFreq, FracBandWidth, SNR):
    tInit = np.linspace(-PulsePeriod*1e-3/2, PulsePeriod*1e-3/2, 2 * Res, endpoint=False)
    SeedSignal = sp.signal.gausspulse(tInit, fc=RadioFreq, bw=FracBandWidth)
    signalArray = []
    signalTime = []
    s = []
    for x in range(0, PulseNum):
        signalArray = np.append(signalArray,np.random.normal(0, 1/SNR, 2*Res)*SeedSignal+np.random.normal(0, 1/SNR, 2*Res))
        s = np.linspace(-PulsePeriod*1e-3/2 + 2*PulsePeriod*1e-3/2*x, PulsePeriod*1e-3/2 + 2*PulsePeriod*1e-3/2*x, 2 * Res, endpoint=False)
        signalTime = np.append(signalTime, s)
    return signalTime, signalArray

t, x = GaussPulseTrain(3, fs, 50., 200, 0.5)


N = len(t)

# Frequency shift:
f_shift = 2

# Shift signal's frequency components by using the Hilbert transform
# to perform SSB modulation:
x_shift = freq_shift(x, f_shift, dt)

# Plot results:
f = np.fft.fftfreq(N, dt)
xf = np.fft.fft(x).real
xf_shift = np.fft.fft(x_shift).real
start = 0
stop = int((45.0/(fs/2.0))*(N/2.0))


plt.clf()
plt.figure(figsize=(24,6))
plt.subplot2grid((2, 3), (0, 0), rowspan=2, colspan=2)
plt.plot(t, x, 'b', t, x_shift, 'r-')
plt.xlabel('t (s)')
plt.ylabel('x(t)')
plt.legend(('original', 'shifted'))
plt.subplot2grid((2, 3), (0, 2))
plt.stem(f[start:stop], xf[start:stop])
plt.title('Original')
plt.subplot2grid((2, 3), (1, 2))
plt.stem(f[start:stop], xf_shift[start:stop])
plt.title('Shifted')
plt.xlabel('F (Hz)')
plt.tight_layout()
plt.suptitle('Frequency Shifting Using SSB Modulation')

plt.draw()
plt.show()
