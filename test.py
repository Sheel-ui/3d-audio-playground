import pygame
import sys
import random
from sound import play_wav_thread
from components import Button,Input

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
LIGHT_BORDER = (130,130,130)
DELETE_BORDER = BORDER
INPUT_BORDER = BORDER
RED = (250,50,5)
MAROON = (230,30,0)
RADIUS = 10
NAVBAR_WIDTH = 200

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

# UI parameters
partition = pygame.Rect(0, 300, 200, 2)

# method similar to collide points
def is_inside_rect(x, y, rect):
    return rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]

def create_thread(filename):
    temp = filename.strip()
    if temp:
        speaker_x = random.randint(NAVBAR_WIDTH, WIDTH - speaker_image.get_width())
        speaker_y = random.randint(0, HEIGHT - speaker_image.get_height())
        speakers[temp] = (speaker_x, speaker_y)
        wav_file = "sample/" + filename  # Path to your wav file
        play_thread, stop_event = play_wav_thread(wav_file)
        threads[filename] = (play_thread, stop_event)

# Function to terminate the earliest created thread
def terminate_thread(filename):
    temp = filename.strip()
    if temp and temp in speakers:
        del speakers[temp]
        thread, stop_event = threads[temp]
        del threads[temp]
        stop_event.set()  # Set the event to signal thread termination
        thread.join()  # Wait for the thread to finish

submit_input = Input(10,20,180,30,10,BORDER,LIGHT_BORDER,"",WHITE)
submit_button = Button(55,70,90,30,10,BLUE,NAVY,"Submit",WHITE,create_thread,submit_input)

delete_input = Input(10,320,180,30,10,BORDER,LIGHT_BORDER,"",WHITE)
delete_button = Button(55,370,90,30,10,RED,MAROON,"Delete",WHITE,terminate_thread,delete_input)
# game is running, dragging set to true when mouse button is down and selected a speaker
running = True
dragging = False
while running:

    for event in pygame.event.get():
        
        submit_button.handle_event(event)
        delete_button.handle_event(event)
        submit_input.read(event,submit_button)
        delete_input.read(event,delete_button)

        if event.type == pygame.QUIT:
            running = False
        # check for button click: submit/delete input; submit/delete button; speaker
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for speaker in speakers.items():
                speaker_rect = pygame.Rect(speaker[1][0], speaker[1][1], speaker_image.get_width(), speaker_image.get_height())
                if is_inside_rect(mouse_x, mouse_y, speaker_rect):
                    delete_button.target.text = speaker[0]
                    dragging = True
                    speaker_index = speaker[0]
                    speaker_offset_x = mouse_x - speaker[1][0]
                    speaker_offset_y = mouse_y - speaker[1][1]
        # stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
    
    # update location if dragging
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        speaker_x = mouse_x - speaker_offset_x
        speaker_y = mouse_y - speaker_offset_y
        speaker_x = max(NAVBAR_WIDTH, min(WIDTH - speaker_image.get_width(), speaker_x))
        speaker_y = max(0, min(HEIGHT - speaker_image.get_height(), speaker_y))
        speakers[speaker_index] = (speaker_x, speaker_y)

    # move the character
    keys = pygame.key.get_pressed()

    # set moving left to true and flip the image
    if keys[pygame.K_LEFT]:
        player_x = max(NAVBAR_WIDTH, player_x - player_speed)
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
    pygame.draw.rect(screen, GRAY, (0, 0, NAVBAR_WIDTH, HEIGHT))

    # partition
    pygame.draw.rect(screen, BORDER, partition)
    
    submit_button.draw(screen)
    delete_button.draw(screen)
    submit_input.draw(screen)
    delete_input.draw(screen)
    
    delete_button.hover()
    submit_button.hover()
    

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
