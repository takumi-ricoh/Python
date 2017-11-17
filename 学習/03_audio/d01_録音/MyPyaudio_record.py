# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 19:37:22 2016

@author: p000495138
"""

import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2**11
RECORD_SECONDS = 10
WAVW_OUTPUT_FILENAME = 'file.wav'

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT,channels = CHANNELS, 
                    rate=RATE, input=True,
                    input_device_index=6,
                    frames_per_buffer=CHUNK)
print("recording...")

#frames=[]
#for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
#    data = stream.read(CHUNK)
#    frames.append(data)
#print("finished recording")
#
#stream.stop_stream()
#stream.close()
#audio.terminate()

