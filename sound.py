import pygame
import threading
import pyaudio
import wave
import numpy as np
import scipy.signal
from variables import speakerVar as var
import math


p = pyaudio.PyAudio()
CHUNK = 30000
power = 5

# Play wav file on loop
def play_wav(filename, stop_event):
    overlapAmount = var.speaker_var[filename].FIRs.shape[2]-1
    dataPrepend = np.zeros(overlapAmount)
    hrtfList = [[0,0]] 
    currentTetraIndex = 0

    wf = wave.open('sample/'+filename, 'rb')
    
    def callback(in_data, frame_count, time_info, status):
        nonlocal currentTetraIndex,hrtfList,dataPrepend

        px = np.sin(var.speaker_var[filename].paz)*np.cos(var.speaker_var[filename].pel)*var.speaker_var[filename].pr
        py = np.cos(var.speaker_var[filename].paz)*np.cos(var.speaker_var[filename].pel)*var.speaker_var[filename].pr
        pz = np.sin(var.speaker_var[filename].pel)*var.speaker_var[filename].pr

        pp = np.array((px, py, pz))
        distance = var.speaker_var[filename].distance
        print
        if distance <= 0.15:
            intensity = power / (4 * math.pi * distance**2)*0.5
       
        elif distance <= 1:
            intensity = power / (4 * math.pi * distance**2)       
        else:
            intensity = 0

        i = 0
        while True:
            [g1, g2, g3] = (pp-var.speaker_var[filename].tetraCoords[currentTetraIndex,3])@var.speaker_var[filename].Tinv[currentTetraIndex]
            g4 = 1-g1-g2-g3
            gs = [g1, g2, g3, g4]
            if all(g >= 0 for g in gs) or i>=20000:#len(tetraCoords):
                break
            currentTetraIndex = var.speaker_var[filename].tri.neighbors[currentTetraIndex][gs.index(min(gs))]
            i+=1

        # and get the HRTF associated with pp
        origPosIndex = var.speaker_var[filename].tri.simplices[currentTetraIndex]
        hrtfB = var.speaker_var[filename].FIRs[origPosIndex[1],:,:]
        hrtfA = var.speaker_var[filename].FIRs[origPosIndex[0],:,:]
        hrtfC = var.speaker_var[filename].FIRs[origPosIndex[2],:,:]
        hrtfD = var.speaker_var[filename].FIRs[origPosIndex[3],:,:]

        hrtf = hrtfA*gs[0]+hrtfB*gs[1]+hrtfC*gs[2]+hrtfD*gs[3]

        if not np.array_equal(hrtfList[-1][0], hrtf[0]):
            hrtfList.append(hrtf)

        data = wf.readframes(frame_count)
        data_int = np.frombuffer(data, dtype=np.int16)
        data_int = np.concatenate((dataPrepend, data_int))
        dataPrepend = data_int[-overlapAmount:]

        binaural_left = scipy.signal.fftconvolve(data_int,hrtf[0])
        binaural_right = scipy.signal.fftconvolve(data_int,hrtf[1])

        if len(binaural_left)>0:
            binaural_left = binaural_left[overlapAmount:-overlapAmount] *intensity
            binaural_left = binaural_left.astype(np.int16)

            binaural_right = binaural_right[overlapAmount:-overlapAmount]*intensity
            binaural_right = binaural_right.astype(np.int16)

        binaural = np.empty((binaural_left.size + binaural_right.size,), dtype=np.int16)
        binaural[0::2] = binaural_left
        binaural[1::2] = binaural_right
        data = binaural[:CHUNK*2].tobytes()
            
        return (data, pyaudio.paContinue)

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=2,#wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
        frames_per_buffer=CHUNK,
        start = False,
        stream_callback=callback)
    
    var.streams[filename] = stream
    
    stream.start_stream()

# Play on thread
def play_wav_thread(filename):
    stop_event = threading.Event()
    thread = threading.Thread(target=play_wav, args=(filename, stop_event))
    thread.start()
    return thread, stop_event