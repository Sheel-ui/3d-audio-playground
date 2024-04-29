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

# Function to play a WAV file with spatialized audio
def play_wav(filename, stop_event):
    overlapLength = var.speaker_var[filename].hrtfData.shape[2]-1
    initialData = np.zeros(overlapLength)
    hrtfList = [[0,0]] 
    tIndex = 0

    # Open WAV file
    wf = wave.open('sample/'+filename, 'rb')
    
    # Callback function for audio stream
    def callback(in_data, frame_count, time_info, status):
        nonlocal initialData,tIndex,hrtfList
        
        # Calculate x, y, and z coordinates of the speaker relative to the listener
        xCoordinate = np.sin(var.speaker_var[filename].speakerAzimuth)*np.cos(var.speaker_var[filename].speakerElevation)*var.speaker_var[filename].speakerDistance
        yCoordinate= np.cos(var.speaker_var[filename].speakerAzimuth)*np.cos(var.speaker_var[filename].speakerElevation)*var.speaker_var[filename].speakerDistance
        zCoordinate = np.sin(var.speaker_var[filename].speakerElevation)*var.speaker_var[filename].speakerDistance

        # Create a numpy array to store the speaker coordinates
        coordinates= np.array((xCoordinate, yCoordinate, zCoordinate))
        distance = var.speaker_var[filename].distance
        
        # Setting intensity based on distance between speaker and character
        if distance <= 0.15:
            intensity = power / (4 * math.pi * distance**2)*0.5
       
        elif distance <= 1:
            intensity = power / (4 * math.pi * distance**2)       
        else:
            intensity = 0

        i = 0
        while True:
            [barycentricCoordinate1, barycentricCoordinate2, barycentricCoordinate3] = (coordinates-var.speaker_var[filename].tetraCoordinates[tIndex,3])@var.speaker_var[filename].tetrahedronInverse[tIndex]
            barycentricCoordinate4 = 1-barycentricCoordinate1-barycentricCoordinate2-barycentricCoordinate3
            barycentricCoordinates = [barycentricCoordinate1, barycentricCoordinate2, barycentricCoordinate3, barycentricCoordinate4]
            if all(c >= 0 for c in barycentricCoordinates) or i>=20000:
                break
            tIndex = var.speaker_var[filename].delaunayTriangulation.neighbors[tIndex][barycentricCoordinates.index(min(barycentricCoordinates))]
            i+=1

        # Find the HRTF values for the current speaker coordinates
        positionIndex = var.speaker_var[filename].delaunayTriangulation.simplices[tIndex]
        hrtfA = var.speaker_var[filename].hrtfData[positionIndex[0],:,:]
        hrtfB = var.speaker_var[filename].hrtfData[positionIndex[1],:,:]
        hrtfC = var.speaker_var[filename].hrtfData[positionIndex[2],:,:]
        hrtfD = var.speaker_var[filename].hrtfData[positionIndex[3],:,:]

        hrtf = hrtfA*barycentricCoordinates[0]+hrtfB*barycentricCoordinates[1]+hrtfC*barycentricCoordinates[2]+hrtfD*barycentricCoordinates[3]

        # Append new HRTFs to list if different from previous
        if not np.array_equal(hrtfList[-1][0], hrtf[0]):
            hrtfList.append(hrtf)

        # Read audio data from WAV file
        data = wf.readframes(frame_count)
        data_int = np.frombuffer(data, dtype=np.int16)
        data_int = np.concatenate((initialData, data_int))
        initialData = data_int[-overlapLength:]

        # Convolve audio data with HRTF to spatialize sound
        left_audio_data = scipy.signal.fftconvolve(data_int,hrtf[0])
        right_audio_data = scipy.signal.fftconvolve(data_int,hrtf[1])
        # Apply intensity and convert to 16-bit integers
        if len(left_audio_data)>0:
            left_audio_data = left_audio_data[overlapLength:-overlapLength] *intensity
            left_audio_data = left_audio_data.astype(np.int16)

            right_audio_data = right_audio_data[overlapLength:-overlapLength]*intensity
            right_audio_data = right_audio_data.astype(np.int16)

        audioData = np.empty((left_audio_data.size + right_audio_data.size,), dtype=np.int16)
        audioData[0::2] = left_audio_data
        audioData[1::2] = right_audio_data
        data = audioData[:CHUNK*2].tobytes()
            
        return (data, pyaudio.paContinue)
    
    # Open audio stream
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=2,#wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
        frames_per_buffer=CHUNK,
        start = False,
        stream_callback=callback)
    
    var.streams[filename] = stream
    
     # Start audio stream
    stream.start_stream()

# Function to play WAV file on a separate thread
def play_wav_thread(filename):
    stop_event = threading.Event()
    thread = threading.Thread(target=play_wav, args=(filename, stop_event))
    thread.start()
    return thread, stop_event