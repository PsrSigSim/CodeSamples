"""pulsar.py
a starting point for the Pulsar class.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np

class Signal(object):
    """the signal class
    """
    self.f0 = None # central freq (MHz)
    self.bw = None # bandwidth (MHz)
    self.Nf = None # number of frequency bins
    self.Nt = None # number of time/phase bins

    self.signal = None # the signal array

    def __init__(self, f0=400, bw=100, Nf=20, Nt=200):
        """initialize Signal(), executed at assignment of new instance
        @param f0 -- central frequecny (MHz)
        @param bw -- bandwidth (MHz)
        @param Nf -- number of freq. bins
        @param Nt -- number of phase bins
        """
        self.f0 = f0 # (MHz)
        self.bw = bw # (MHz)
        self.Nf = Nf # freq bins
        self.Nt = Nt # phase bins

        self.signal = np.zeros((self.Nf, self.Nt))

