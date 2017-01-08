#!/usr/bin/env python3

import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt

transform_size = int(2**13)

# read wave file and make sure that the number of samples in the input signal
# is an integer multiple of the transform size
samp_rate,samples = scipy.io.wavfile.read('wspr.wav')
samples.resize((1,(samples.size//transform_size+1)*transform_size))

# reshape the sample array so that there are transform_size samples per line
# --> FFT can be calculated with a single call to rfft
samples = np.reshape(samples,(samples.size//transform_size,transform_size))
spec = np.abs(np.fft.rfft(samples,transform_size))

# these plots just show the recovered symbols and a waterfall image
# this needs obviously much more work, figuring out how many FSK signals
# are in the calculated spectra, frequency tracking etc. etc.

# the bin indices used here are precalculated because I have been testing this
# concept with an ideal signal, i.e. all carriers are aligned to the FFT bins
# and there is no frequency drift like you'd see on a real WSPR signal, also
# the signal starts right away not after 1 second (samp_rate number of samples)
plt.figure()
plt.subplot(411)
plt.plot(spec[:,1000])
plt.subplot(412)
plt.plot(spec[:,1001])
plt.subplot(413)
plt.plot(spec[:,1002])
plt.subplot(414)
plt.plot(spec[:,1003])

plt.figure()
plt.imshow(spec,interpolation='none',origin='lower')

plt.show()
