## WSPR Encoding & Decoding shenanigans

This repository holds some of my playing around with WSPR Encoding & Decoding.
Although I have been playing around with this for a while I have discarded most
of that work and wanted to start over.

My digital modulation class this semester really has given me great insight into
the basic principles of modern modulation schemes and I want to try and get a more
practical knowledge of FSK & WSPR through this project.

The project uses Python 3 with the [numpy and scipy](https://www.scipy.org/) modules.

**fft_fsk_demod.py** is the demodulator, based on a 8192-point FFT
**wsprgen.py** generates a wave file with a WSPR encoded message
**WsprMessge.py** class that contains all the methods for encoding a message according
to the resources in [this great PDF](http://g4jnt.com/Coding/WSPR_Coding_Process.pdf) compiled by Andy Talbot, G4JNT.
