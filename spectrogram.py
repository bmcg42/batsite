# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 13:27:47 2021

@author: bpmcg
"""

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import eel

eel.init("web")

@eel.expose
def output_filename(filename):
    print("Hello")
def spectrogram(filename):
    output = 'spectrogram.jpg'
    hop_length = 512
    n_fft = 2048
    #filename = 'music_sample.wav'
    sr = librosa.get_samplerate(filename)

    stream = librosa.stream(filename,
                        block_length=256,
                        frame_length=2048,
                        hop_length=2048)

    for y_block in stream:
        D = np.abs(librosa.stft(y_block, n_fft=n_fft,  hop_length=hop_length))

        DB = librosa.amplitude_to_db(D, ref=np.max)

    librosa.display.specshow(DB, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log');
    plt.colorbar(format='%+2.0f dB')
    plt.savefig(output)
    return(output)

eel.start("index.html")