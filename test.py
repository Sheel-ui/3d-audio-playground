import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Character Movement")
background_image = pygame.image.load("assets/background.png")

character_images = [
    pygame.image.load("assets/mario1.png"),
    pygame.image.load("assets/mario2.png")  
]
speaker_image = pygame.image.load("assets/speaker.png")

WHITE = (255,255,255)
GRAY = (50, 50, 50)

character_size = 50
player_x = (WIDTH - character_size) // 2
player_y = (HEIGHT - character_size) // 2
player_speed = 3
speakers = []
animation_delay = 5
animation_counter = 0
character_index = 0

navbar_width = 200

button_width, button_height = 150, 50
button_x, button_y = 25, 275
button_color = (50, 150, 255)

def is_inside_rect(x, y, rect):
    return rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]

def is_inside_image(x, y, image):
    image_width, image_height = image.get_size()
    return 0 <= x <= image_width and 0 <= y <= image_height

font = pygame.font.Font(None, 30)
text = font.render("Add Speaker", True, WHITE)

running = True
dragging = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if is_inside_rect(mouse_x, mouse_y, (button_x, button_y, button_width, button_height)):
                speaker_x = random.randint(navbar_width, WIDTH - speaker_image.get_width())
                speaker_y = random.randint(0, HEIGHT - speaker_image.get_height())
                speakers.append((speaker_x, speaker_y))  # Add speaker position to the list
            else:
                for index, speaker in enumerate(speakers):
                    speaker_rect = pygame.Rect(speaker[0], speaker[1], speaker_image.get_width(), speaker_image.get_height())
                    if is_inside_rect(mouse_x, mouse_y, speaker_rect):
                        dragging = True
                        speaker_index = index
                        speaker_offset_x = mouse_x - speaker[0]
                        speaker_offset_y = mouse_y - speaker[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        speaker_x = mouse_x - speaker_offset_x
        speaker_y = mouse_y - speaker_offset_y
        speaker_x = max(navbar_width, min(WIDTH - speaker_image.get_width(), speaker_x))
        speaker_y = max(0, min(HEIGHT - speaker_image.get_height(), speaker_y))
        speakers[speaker_index] = (speaker_x, speaker_y)

    keys = pygame.key.get_pressed()

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

    if animation_counter >= animation_delay:
        character_index = (character_index + 1) % len(character_images)
        animation_counter = 0

    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, GRAY, (0, 0, navbar_width, HEIGHT))

    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    screen.blit(text, (button_x + 12, button_y + 15))

    character_image = character_images[character_index]
    if moving_left:
        character_image = pygame.transform.flip(character_image, True, False)
    screen.blit(character_image, (player_x, player_y))

    for speaker in speakers:
        screen.blit(speaker_image, (speaker[0], speaker[1]))

    pygame.display.update()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
