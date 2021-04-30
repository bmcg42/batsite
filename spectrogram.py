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
import base64
from os import remove
from os.path import dirname, realpath, join, isfile

eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose
def output_filename(filename):
    print('Hello')
    
@eel.expose
def spectrogram(filename, output_fn):
    if not output_fn.startswith('web/'):
        output = 'web/' + output_fn
    else:
        output = output_fn
    if not output.endswith('.jpg'):
        output += '.jpg'

    if isfile(output):
        remove(output)

    hop_length = 512
    n_fft = 2048
    
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

    plt.close()
    with open(output, 'rb') as output:
        byte_string = base64.b64encode(output.read())
        return byte_string.decode('ascii')
   
eel.start("index.html")