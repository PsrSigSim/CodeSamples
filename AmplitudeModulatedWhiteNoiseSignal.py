#!/usr/bin/env python
"""
Amplitude Modulated white noise.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import scipy as sp
import scipy.signal
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

dt = 1e-2 #Fraction of a millisecond
fs = int(1/dt)

#Resolution is set above at 10e-5 sec
#PulsePeriod is given in milliseconds

"""
The function below uses a gaussian window to modulate white noise. Currently
the number of pulses is dictated explictly, but in the future it would be
calculated from the time elapsed and period. 
"""

def GaussPulseTrain(PulseNum, Res, PulsePeriod, SNR, GaussWidth):
    tInit = np.linspace(-PulsePeriod*1e-3/2, PulsePeriod*1e-3/2, 2 * Res, endpoint=False)
    SeedSignal = sp.signal.gaussian(2*Res, GaussWidth)
    signalArray = []
    signalTime = []
    s = []
    for x in range(0, PulseNum):
        signalArray = np.append(signalArray,np.random.normal(0, 1/SNR, 2*Res)*SeedSignal)#+np.random.normal(0, 1/SNR, 2*Res)
        s = np.linspace(-PulsePeriod*1e-3/2 + 2*PulsePeriod*1e-3/2*x, PulsePeriod*1e-3/2 + 2*PulsePeriod*1e-3/2*x, 2 * Res, endpoint=False)
        signalTime = np.append(signalTime, s)
    return signalTime, signalArray

Period = 50. #milliseconds
N = 20
SigmaNoise = 2.
SigmaGauss = 10.

t, x = GaussPulseTrain(N, fs, Period, SigmaNoise, SigmaGauss)


plt.clf()
plt.figure(figsize=(24,6))

plt.subplot2grid((2, 3), (0, 0), rowspan=1, colspan=3)
plt.plot(t, x, 'b')
plt.xlim([-Period*1e-3/2,Period*1e-3/2+2*Period*1e-3/2*(N-1)])
plt.xlabel('t (s)')
plt.ylabel('x')
plt.subplot2grid((2, 3), (1, 0), rowspan=1, colspan=3)
plt.plot(t, x**2, 'r')
plt.xlim([-Period*1e-3/2,Period*1e-3/2+2*Period*1e-3/2*(N-1)])
plt.xlabel('t (s)')
plt.ylabel('Intensity')


plt.draw()
plt.show()
