import pygame
import sys
import random
import threading
import wave

pygame.init()

# screen height width, background, speaker images load
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Character Movement")
background_image = pygame.image.load("assets/background.png")
character_images = [
    pygame.image.load("assets/mario1.png"),
    pygame.image.load("assets/mario2.png")  
]
speaker_image = pygame.image.load("assets/speaker.png")

# BASIC COLORS
WHITE = (255,255,255)
GRAY = (50, 50, 50)
BLACK = (0,0,0)
BLUE = (50, 150, 255)
NAVY = (45,135,220)
BORDER = (80,80,80)
RED = (250,50,5)


# Character size, position, speed, index for selecting image to render
character_size = 50
player_x = (WIDTH - character_size) // 2
player_y = (HEIGHT - character_size) // 2
player_speed = 3
animation_delay = 5
animation_counter = 0
character_index = 0

# Dictionary of speakers and wav threads added added
speakers = {}
threads = {}

# Form for input field and Submit button
font = pygame.font.Font(None, 32)
input_text = ''
input_rect = pygame.Rect(10, 20, 180, 30)
input_active = False                                  # form is inactive when not selected
submit_button_rect = pygame.Rect(55, 70, 90, 30)
rect_radius = 10 
submit_button_color = BLUE


# Partition
partition = pygame.Rect(0, 300, 200, 2)
delete_text = ''
delete_active = False                                # form is inactive when not selected
delete_input = pygame.Rect(10,320,180,30)
delete_rect = pygame.Rect(55, 370, 90, 30)
delete_button_color = RED

# Control panel on the left
navbar_width = 200


# Play wav file on loop
def play_wav(file_path, stop_event):
    wf = wave.open(file_path, 'rb')
    chunk = 1024

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

# method similar to collide points
def is_inside_rect(x, y, rect):
    return rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]

def create_thread(filename):
    wav_file = "sample/" + filename  # Path to your wav file
    play_thread, stop_event = play_wav_thread(wav_file)
    threads[filename] = (play_thread, stop_event)

# Function to terminate the earliest created thread
def terminate_thread(filename):
    if threads:
        thread, stop_event = threads[filename]
        del threads[filename]
        stop_event.set()  # Set the event to signal thread termination
        thread.join()  # Wait for the thread to finish


# will remove this
font = pygame.font.Font(None, 30)
text_button = font.render("Add Speaker", True, WHITE)

# game is running, dragging set to true when mouse button is down and selected a speaker
running = True
dragging = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check for button click: submit/delete input; submit/delete button; speaker
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # submit input
            if input_rect.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
            # delete input
            if delete_input.collidepoint(event.pos):
                delete_active = True
            else:
                delete_active = False
            # submit button
            if submit_button_rect.collidepoint(event.pos):
                temp = input_text.strip()
                if temp:
                    input_text = ''
                    speaker_x = random.randint(navbar_width, WIDTH - speaker_image.get_width())
                    speaker_y = random.randint(0, HEIGHT - speaker_image.get_height())
                    speakers[temp] = (speaker_x, speaker_y)
                    create_thread(temp)
            # delete button
            if delete_rect.collidepoint(event.pos):
                temp = delete_text.strip()
                if temp and temp in speakers:
                    delete_text = ''
                    del speakers[temp]
                    terminate_thread(temp)
            # individaul speaker
            else:
                for speaker in speakers.items():
                    speaker_rect = pygame.Rect(speaker[1][0], speaker[1][1], speaker_image.get_width(), speaker_image.get_height())
                    if is_inside_rect(mouse_x, mouse_y, speaker_rect):
                        delete_text = speaker[0]
                        dragging = True
                        speaker_index = speaker[0]
                        speaker_offset_x = mouse_x - speaker[1][0]
                        speaker_offset_y = mouse_y - speaker[1][1]
        # stop dtagging
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        # text input
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            if delete_active:
                if event.key == pygame.K_BACKSPACE:
                    delete_text = delete_text[:-1]
                else:
                    delete_text += event.unicode
    
    # update location if dragging
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        speaker_x = mouse_x - speaker_offset_x
        speaker_y = mouse_y - speaker_offset_y
        speaker_x = max(navbar_width, min(WIDTH - speaker_image.get_width(), speaker_x))
        speaker_y = max(0, min(HEIGHT - speaker_image.get_height(), speaker_y))
        speakers[speaker_index] = (speaker_x, speaker_y)

    # move the character
    keys = pygame.key.get_pressed()

    # set moving left to true and flip the image
    if keys[pygame.K_LEFT]:
        player_x = max(navbar_width, player_x - player_speed)
        moving_left = True
        animation_counter += 1
    else:
        moving_left = False
    if keys[pygame.K_RIGHT]:
        player_x = min(WIDTH - character_size, player_x + player_speed)
        animation_counter += 1
    if keys[pygame.K_UP]:
        player_y = max(0, player_y - player_speed)
        animation_counter += 1
    if keys[pygame.K_DOWN]:
        player_y = min(HEIGHT - character_size, player_y + player_speed)
        animation_counter += 1

    # change image when counter exceeds delay
    if animation_counter >= animation_delay:
        character_index = (character_index + 1) % len(character_images)
        animation_counter = 0

    # background image and navbar
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, GRAY, (0, 0, navbar_width, HEIGHT))

    # input form
    pygame.draw.rect(screen, BORDER, input_rect, 2,border_radius=rect_radius)
    text_surface = font.render(input_text, True, WHITE)
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # submit form
    pygame.draw.rect(screen, submit_button_color, submit_button_rect, border_radius=rect_radius)
    submit_text = font.render("Submit", True, WHITE)
    screen.blit(submit_text, (submit_button_rect.x + 10, submit_button_rect.y + 5))
    
    # partition
    pygame.draw.rect(screen, BORDER, partition)
    
    # delete form
    pygame.draw.rect(screen, BORDER, delete_input, 2,border_radius=rect_radius)
    text_surface = font.render(delete_text, True, WHITE)
    screen.blit(text_surface, (delete_input.x + 5, delete_input.y + 5))

    # delete button
    pygame.draw.rect(screen, delete_button_color, delete_rect, border_radius=rect_radius)
    submit_text = font.render("Delete", True, WHITE)
    screen.blit(submit_text, (delete_rect.x + 10, delete_rect.y + 5))
    

    # submit logic
    if submit_button_rect.collidepoint(pygame.mouse.get_pos()):
        submit_button_color = NAVY
    else:
        submit_button_color = BLUE

    # character render
    character_image = character_images[character_index]
    if moving_left:
        character_image = pygame.transform.flip(character_image, True, False)
    screen.blit(character_image, (player_x, player_y))

    # speaker render
    for speaker in speakers.values():
        screen.blit(speaker_image, (speaker[0], speaker[1]))
        
        

    pygame.display.update()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
