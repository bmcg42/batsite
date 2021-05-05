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
import pandas as pd
import acoustics as ac

eel.init('web', allowed_extensions=['.js', '.html'])

def find_zeros(block):
    for i in range(len(block)):
        if not block[i]:
            block[i] = 0.000001
    return block
    
@eel.expose                         #expose function to main.js
def SPL_Table(filename):
    #start stream
    stream = librosa.stream(filename,
                        block_length=256,
                        frame_length=2048,
                        hop_length=2048)
    #calculate spl of each block
    bcount = 0
    for block in stream:
        block = find_zeros(block)
        spl = ac.descriptors.sound_pressure_level(block)
        avg = np.average(spl)
        if not bcount:
            c1 = np.array(avg)
            count = np.array(bcount+1)
        else:
            c1 = np.append(c1,avg)
            count = np.append(count, bcount+1)
        bcount+=1

    #convert to table
    spl_table =  pd.DataFrame({
        #'title' : array_name #creates column
        'SPL' : c1
    })
    spl_table.index = count
    spl_table.index.name='Block Number'
    return spl_table.to_html()

@eel.expose                     
def spectrogram(filename): 
    #sample rate
    sr = librosa.get_samplerate(filename)
    #start stream
    stream = librosa.stream(filename,
                        block_length=256,
                        frame_length=2048,
                        hop_length=2048)
    output = 'web/output.jpg'
    if isfile(output):
        remove(output)        
    #spectrogram properties
    hop_length = 512
    n_fft = 2048
    
    #calculate spectrogram data
    bcount = 0
    for y_block in stream:
        D = np.abs(librosa.stft(y_block, n_fft=n_fft,  hop_length=hop_length))
        DB=librosa.amplitude_to_db(D, ref=np.max)
        if not bcount:
            output_array = DB
        else:
            output_array = np.hstack((output_array,DB))
        bcount+=1
    #show spectrogram
    fig, ax =  plt.subplots(figsize = (5*bcount,5))
    librosa.display.specshow(output_array, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log',ax = ax)
    #plt.colorbar(format='%+2.0f dB')
    plt.savefig(output)

    plt.close()
    #write saved spectrogram fig to ascii string to be read by main.js & index.html
    with open(output, 'rb') as output:
        byte_string = base64.b64encode(output.read())
        return byte_string.decode('ascii')
   
eel.start("index.html")
