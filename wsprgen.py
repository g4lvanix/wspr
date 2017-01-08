#!/usr/bin/env python3

import numpy as np
import scipy.io.wavfile
import WsprMessage

# for debug purposes only
import matplotlib.pyplot as plt

# define sample rate and normalized carrier & symbol offset frequency
samp_rate = 12000
fc = 1000/8192
df = 1/8192

# encode my call, locator and TX power according to WSPR message packing standard
msg = WsprMessage.WsprMessage("DL1YE","JO61",37)
# generate the signal, note this is not CPFSK as defined by WSPR, still have
# to implement that
t = np.arange(8192)
sig = np.array([])

for cs in msg.channelSymbols():
	sig = np.concatenate((sig,np.cos(2*np.pi*(fc+cs*df)*t)))

# write the signal to a wave file for further processing
scipy.io.wavfile.write('wspr.wav',samp_rate,np.array(sig,dtype='float32'))
