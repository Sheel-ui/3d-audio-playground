import pygame
import threading

# Play wav file on loop
def play_wav(file_path, stop_event):

    stream = pygame.mixer.Sound(file=file_path)
    stream.play(-1)                                 # plat on loop

    while not stop_event.is_set():
        pygame.time.delay(100)  # A short delay to prevent busy waiting

    stream.stop()

# Play on thread
def play_wav_thread(file_path):
    stop_event = threading.Event()
    thread = threading.Thread(target=play_wav, args=(file_path, stop_event))
    thread.start()
    return thread, stop_event