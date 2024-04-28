import pygame
import sys
import random
from sound import play_wav_thread
from components import Button,Input, Circle, Plot, Text
from variables import Variables
from variables import speakerVar as var
import numpy as np
import os

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
TEXT = (180,180,180)

# Character size, position, speed, index for selecting image to render
character_size = 50
player_x = (WIDTH - character_size) // 2
player_y = (HEIGHT - character_size) // 2
player_speed = 3
animation_delay = 5
animation_counter = 0
character_index = 0
shadow_radius = 200
shadow_color = (255, 255, 255, 30)
shadow = pygame.Surface((shadow_radius * 2, shadow_radius * 2), pygame.SRCALPHA)
curradius = 6
elCursor = pygame.Surface((curradius*2,curradius*2),pygame.SRCALPHA)
rCursor =pygame.Surface((curradius*2,curradius*2),pygame.SRCALPHA)
elCursor_x,elCursor_y = 26,505
rCursor_x, rCursor_y = 135,441
selectedHrtf = "1"

moving_left = False
# Dictionary of speakers and wav threads added added
speakers = {}
threads = {}

# UI parameters
partition = pygame.Rect(0, 275, 200, 2)
minR = 0.075
# method similar to collide points
def is_inside_rect(x, y, rect):
    return rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]

def getDistance(speaker_x,speaker_y):
        x1, y1 = speaker_x+speaker_image.get_width()//2,speaker_y+speaker_image.get_height()//2
        x2, y2 = player_x+character_size//2,player_y+character_size//2
        return ((y2-y1)**2 +(x2-x1)**2)**0.5

def hrtfParams(speaker_x,speaker_y):
    x1, y1 = speaker_x+speaker_image.get_width()//2,speaker_y+speaker_image.get_height()//2
    x2, y2 = player_x+character_size//2,player_y+character_size//2
    distance = ((y2-y1)**2 +(x2-x1)**2)**0.5
    distance = distance/200 + minR
    return distance

def create_thread(filename):
    global elCursor_y, rCursor_x
    temp = filename.strip()
    path = 'sample/'+temp
    if os.path.exists(path):
        texts[6] = ""
        speaker_x = random.randint(NAVBAR_WIDTH, WIDTH - speaker_image.get_width())
        speaker_y = random.randint(0, HEIGHT - speaker_image.get_height())
        elCursor_y = 505
        rCursor_x = 135
        speakers[temp] = (speaker_x, speaker_y,elCursor_y,rCursor_x)
        distance = hrtfParams(speaker_x,speaker_y)
        var.speaker_var[filename]=Variables(distance,selectedHrtf)
        play_thread, stop_event = play_wav_thread(filename)
        threads[filename] = (play_thread, stop_event)
    else:
        texts[6] = "File Doesn't Exists"

# Function to terminate the earliest created thread
def terminate_thread(filename):
    global elCursor_y, rCursor_x
    temp = filename.strip()
    if temp and temp in speakers:
        del speakers[temp]
        thread, stop_event = threads[temp]
        del threads[temp]
        stop_event.set()  # Set the event to signal thread termination
        thread.join()  # Wait for the thread to finish
        stream = var.streams[filename]
        stream.stop_stream()
        elCursor_y = 505
        rCursor_x = 135
        del var.streams[filename]

submit_input = Input(10,46,180,30,10,BORDER,LIGHT_BORDER,"",WHITE)
submit_button = Button(55,190,90,30,10,BLUE,NAVY,"Submit",WHITE,create_thread,submit_input)

delete_input = Input(10,321,180,30,10,BORDER,LIGHT_BORDER,"",WHITE)
delete_button = Button(55,540,90,30,10,RED,MAROON,"Delete",WHITE,terminate_thread,delete_input)

elPlot = Plot(30,385,4, 120,LIGHT_BORDER)
rPlot = Plot(52,445, 120, 4,LIGHT_BORDER)

hrtfA = Circle(16,125,15,LIGHT_BORDER,BLUE,"1",WHITE)
hrtfB = Circle(62,125,15,LIGHT_BORDER,BLUE,"2",WHITE)
hrtfC = Circle(108,125,15,LIGHT_BORDER,BLUE,"3",WHITE)
hrtfD = Circle(154,125,15,LIGHT_BORDER,BLUE,"4",WHITE)

# Define texts, positions, font sizes, and colors
texts = ["Add Source", "Select HRTF Profile", "Edit Source", "Elevation", "Radius","of the Head",""]
positions = [(15, 20), (15, 96), (15, 295), (8, 365), (90, 460), (78,472),(15,80)]
font_sizes = [24, 24, 24,18,18,18,16]
colors = [TEXT, TEXT, TEXT,TEXT,TEXT,TEXT,RED]

# Create a Text object
text_object = Text(texts, positions, font_sizes, colors)



# game is running, dragging set to true when mouse button is down and selected a speaker

speaker_index = ""
running = True
dragging = False
rActive, elActive = False, False

def hrtfClick(event,circle):
    global selectedHrtf
    temp = circle.click(event,selectedHrtf)
    if temp!=selectedHrtf:
        selectedHrtf = temp
        hrtfA.color = LIGHT_BORDER
        hrtfB.color = LIGHT_BORDER
        hrtfC.color = LIGHT_BORDER
        hrtfD.color = LIGHT_BORDER
    if temp=="1":
        hrtfA.color = BLUE
    elif temp=="2":
        hrtfB.color = BLUE
    elif temp=="3":
        hrtfC.color = BLUE
    elif temp=="4":
        hrtfD.color = BLUE

while running:

    for event in pygame.event.get():
        submit_button.handle_event(event)
        delete_button.handle_event(event)
        submit_input.read(event,submit_button)
        delete_input.read(event,delete_button)
        hrtfClick(event,hrtfA)
        hrtfClick(event,hrtfB)
        hrtfClick(event,hrtfC)
        hrtfClick(event,hrtfD)

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
                    elCursor_y = speaker[1][2]
                    rCursor_x = speaker[1][3]
                    speaker_offset_x = mouse_x - speaker[1][0]
                    speaker_offset_y = mouse_y - speaker[1][1]

            rCursorRect = pygame.Rect(rCursor_x, rCursor_y,10,10)
            elCursorRect = pygame.Rect(elCursor_x, elCursor_y,10,10)

            if is_inside_rect(mouse_x, mouse_y, rCursorRect) and len(delete_input.text):                 
                rActive = True
                
            if is_inside_rect(mouse_x, mouse_y, elCursorRect) and len(delete_input.text): 
                elActive = True       
                    
        # stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            rActive, elActive = False, False
    
    # update location if dragging
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        speaker_x = mouse_x - speaker_offset_x
        speaker_y = mouse_y - speaker_offset_y
        speaker_x = max(NAVBAR_WIDTH, min(WIDTH - speaker_image.get_width(), speaker_x))
        speaker_y = max(0, min(HEIGHT - speaker_image.get_height(), speaker_y))
        speakers[speaker_index] = (speaker_x, speaker_y,speakers[speaker_index][2],speakers[speaker_index][3])
        var.speaker_var[speaker_index].azimuth = np.arctan2(speaker_y-player_y, speaker_x-player_x)+np.pi/2
        var.speaker_var[speaker_index].distance  = hrtfParams(speaker_x, speaker_y)
        # print("Elevation: ",var.speaker_var[speaker_index].elevation)
        # # print("R: ",var.speaker_var[speaker_index].dist )
       
    if elActive:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        elCursor_y = mouse_y
        elCursor_x = 26
        if elCursor_y > 505:
            elCursor_y = 505
        elif elCursor_y < 385:
            elCursor_y = 385
        speaker_index = delete_input.text.strip()
        speakers[speaker_index] = (speakers[speaker_index][0], speakers[speaker_index][1],elCursor_y,speakers[speaker_index][3])
        ele = (505-speakers[speaker_index][2])/120*140-50
        var.speaker_var[speaker_index].elevation = ele*np.pi/180
        # print("Elevation: ",var.speaker_var[speaker_index].elevation) 
      
    if rActive:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rCursor_x = mouse_x
        rCursor_y = 441
        if rCursor_x > 172:
            rCursor_x = 172
        elif rCursor_x < 52:
            rCursor_x = 52
        speaker_index = delete_input.text.strip()
        speakers[speaker_index] = (speakers[speaker_index][0], speakers[speaker_index][1],speakers[speaker_index][2],rCursor_x)
        var.speaker_var[speaker_index].dist = (rCursor_x-51)/120*(3.325) + minR  #maxR = 3.4, minR=0.075
        # print("R: ",var.speaker_var[speaker_index].dist ) 
     
    # move the character
    keys = pygame.key.get_pressed()

    # set moving left to true and flip the image
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        if keys[pygame.K_LEFT]:
            player_x = max(NAVBAR_WIDTH, player_x - player_speed)
            moving_left = True
            animation_counter += 1
        else:
            moving_left = False
        if keys[pygame.K_RIGHT]:
            player_x = min(WIDTH - character_size//2, player_x + player_speed)
            animation_counter += 1
        if keys[pygame.K_UP]:
            player_y = max(0, player_y - player_speed)
            animation_counter += 1
        if keys[pygame.K_DOWN]:
            player_y = min(HEIGHT - character_size//2, player_y + player_speed)
            animation_counter += 1
            
        for speaker in speakers.items():
            speaker_index = speaker[0]
            speaker_x, speaker_y = speaker[1][0], speaker[1][1]
            var.speaker_var[speaker_index].azimuth = np.arctan2(speaker_y-player_y, speaker_x-player_x)+np.pi/2
            var.speaker_var[speaker_index].distance  = hrtfParams(speaker_x, speaker_y)
            # var.speaker_var[speaker_index].elevation = (505-speakers[speaker_index][2])/120*140-50
            # var.speaker_var[speaker_index].dist = (600-abs(player_x-speaker_x))/600*(var.speaker_var[speaker_index].maxR-minR) + minR
                    
    for speaker in speakers.items():
        s = speaker[0]
        var.speaker_var[s].speakerAzimuth= -var.speaker_var[s].azimuth
        var.speaker_var[s].speakerElevation = var.speaker_var[s].elevation
        var.speaker_var[s].pr = var.speaker_var[s].dist

    # change image when counter exceeds delay
    if animation_counter >= animation_delay:
        character_index = (character_index + 1) % len(character_images)
        animation_counter = 0

   
    # background image and navbar
    screen.blit(background_image, (0, 0))
    
    # character render
    character_image = character_images[character_index]
   
    if moving_left:
        character_image = pygame.transform.flip(character_image, True, False)
    screen.blit(character_image, (player_x, player_y))

    pygame.draw.circle(shadow, shadow_color, (shadow_radius, shadow_radius), shadow_radius)
    screen.blit(shadow, (player_x - shadow_radius + character_size//4, player_y - shadow_radius+character_size//2))
    
    pygame.draw.circle(elCursor,BLUE,(curradius,curradius),curradius)
    pygame.draw.circle(rCursor,BLUE,(curradius,curradius),curradius)
    
    # speaker render
    for speaker in speakers.values():
        screen.blit(speaker_image, (speaker[0], speaker[1]))
    
    pygame.draw.rect(screen, GRAY, (0, 0, NAVBAR_WIDTH, HEIGHT))
    submit_button.draw(screen)
    delete_button.draw(screen)
    submit_input.draw(screen)
    delete_input.draw(screen)
    delete_button.hover()
    submit_button.hover()
    pygame.draw.rect(screen, BORDER, partition)

    elPlot.draw(screen)
    rPlot.draw(screen)
    
    screen.blit(elCursor,(elCursor_x,elCursor_y))
    screen.blit(rCursor,(rCursor_x,rCursor_y))

    hrtfA.draw(screen)
    hrtfB.draw(screen)
    hrtfC.draw(screen)
    hrtfD.draw(screen)
    
    text_object.draw(screen)

    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
