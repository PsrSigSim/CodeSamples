#!/usr/bin/env python
"""draw_sing_puls.py
draw several single pulses from an average profile
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import matplotlib.pyplot as plt

def gauss_template(peak=0.25, width=0.05, amp=1., nbins=100):
    """template(peak, width, nbins)
    generate a gaussian or sum of gaussians profile template
    @param peak  -- mean of gaussian (or array for sum of several)
    @param width -- stdev of gaussian (or arroy for sum of several)
    @param amp   -- amp of gaussian (or arroy for sum of several)
    return intesity profile and sample phases of template
    """
    #TODO: error checking for array length consistency?
    #TODO: if any param is a not array, then broadcast to all entries of other arrays?
    phase = np.linspace(0., 1., nbins)
    try: # is this an array
        peak = np.array(peak)
        width = np.array(width)
        amp = np.array(amp)
        amp = amp/amp.sum()  # normalize sum
        profile = np.zeros(nbins)
        for ii in range(amp.size):
            norm = amp[ii]/np.sqrt(2.*np.pi)/width[ii]
            profile += norm * np.exp(-0.5 * ((phase-peak[ii])/width[ii])**2)
    
    except: # one gaussian
        norm = 1./np.sqrt(2.*np.pi)/width
        profile = norm * np.exp(-0.5 * ((phase-peak)/width)**2)

    return (phase, profile)

def draw_pulse(phase, profile, nbins):
    """draw_pulse(phase, pulse, nbins)
    draw a single pulse as bin by bin random process (gamma distr) from input template
    """
    #TODO: draw pulse at arbitrary sample rate (presumed less than template?)
    #TODO: phase and nbins do nothing until this is finished
    #TODO: average template into new phase bins
    ph = np.linspace(0., 1., nbins) # new phase bins
    pr = profile
    pulse = np.random.gamma(4., pr/4.)
    
    #TODO: interpolate single pulse back to full resolution

    return pulse

###########
## SETUP ##
###########
Npulse = 100
Nbins = 50
Peak = [0.30, 0.20]
wid = [0.05, 0.04]
amp = [1., 2.]

pulses = np.zeros((Npulse, Nbins))

###########
## DO IT ##
###########
# generate template
phas, prof = gauss_template(peak=Peak, width=wid, amp=amp, nbins=Nbins)

# draw pulse from template
for ii in range(Npulse):
    pulses[ii] = draw_pulse(phas, prof, nbins=Nbins)

# compute average of single pulses
mean_profile = pulses.mean(axis=0)


###########
## PLOTS ##
###########
bbox = [0.10, 0.10, 0.85, 0.85]

# plot average & template
fig = plt.figure()
ax = fig.add_axes(bbox)
ax.plot(phas, prof, 'k--', label='template')
ax.plot(phas, mean_profile, 'b-', label='mean profile')
ax.set_xlabel('phase')
ax.set_ylabel('intensity')
ax.legend()
fig.savefig("mean_profile.pdf")

# plot single pulses "Joy Division" style
fig = plt.figure()
ax = fig.add_axes(bbox)
for ii in range(Npulse):
    ax.plot(phas, 3*(ii+1)+pulses[ii], 'k-')
ax.set_xlabel('phase')
ax.set_yticklabels([])
fig.savefig("single_pulses.pdf")


