# ----------------------------------------------------------------
# PACMAN UNFINISHED
# By Rafael Sanchez
# Description: A clone of the classic arcade.
# ----------------------------------------------------------------
# Code is devided in sections
# ------------------------------------------------- ESSENTIALS ------------------------------------------------------- 
# Imports go here
import pygame
from pygame import mixer
import os

# Here import the buttons that you want from pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_UP,
    K_RETURN,
    K_ESCAPE,
    QUIT,
)

# Insert Game Title
GAME_TITLE = "PACMAN"

# Here initialize the game. Leave this alone.
pygame.init()
pygame.font.init()
mixer.init()

# Change game Icon for window
programIcon = pygame.image.load('Data'+os.sep+'ikon.png')
pygame.display.set_icon(programIcon)

# Define some playtesting colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define size of Game Window
WID = 800
HEI = 600

# Width and Height of the screen are initialized
size = (WID, HEI)
screen = pygame.display.set_mode(size)

# Display Game Title
pygame.display.set_caption(GAME_TITLE)

# Define the fonts to be used in-game
F = 'Data'+os.sep+'ARCADECLASSIC.TTF'
MAX_SIZE = 100
SIZES = [int(MAX_SIZE*0.2), int(MAX_SIZE*0.4), int(MAX_SIZE*0.6), int(MAX_SIZE*0.8), MAX_SIZE]

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# ------------------------------------------------- ESSENTIALS ------------------------------------------------------- 
# ------------------------------------------------- USEFUL -----------------------------------------------------------
# Define variables for game logic here 


# The Sound Function, which plays all sounds in game. Call this to play sounds or music. Returns 0 on success for playing music, and a Sound if playing sounds.
def sound_master(soundFilePath, isMusic, onLoop):
    sound = 0
    if not isMusic:
        sound = mixer.Sound(soundFilePath)
    if isMusic:
        mixer.music.load(soundFilePath)
        mixer.music.set_volume(0.7)
        if onLoop:
            mixer.music.play(-1)
        else:
            mixer.music.play()
    else:
        if onLoop:
            sound.play(-1)
        else:
            sound.play()
    return sound

# Define useful functions for the game here
def font_master(pathFont, font_size, textDrawn, antiAlias, color, centerItForMe, offset_x, offset_y):
    font = pygame.font.Font(pathFont, font_size)
    text = font.render(textDrawn, antiAlias, color)
    textRect = text.get_rect()
    if centerItForMe:
        textRect.topleft = (WID//2-textRect.width//2+offset_x, HEI//2-textRect.width//2+offset_y)
    else:
        textRect.topleft = (offset_x, offset_y)
    screen.blit(text, textRect)




# Objects, Classes, Players, Enemies, everything of that sort

# Initialize other varibles, classes (Optional)

# ------------------------------------------------- USEFUL -----------------------------------------------------------
# ------------------------------------------------- GAME LOGIC & EVERYTHING ------------------------------------------
counter = 0
done = False
while not done:
    # Main event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
 
        # Player Inputs
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            pass
        if keys[K_RIGHT]:
            pass
        if keys[K_DOWN]:
            pass
        if keys[K_UP]:
            pass
        if keys[K_RETURN]:
            pass
        if keys[K_ESCAPE]:
            done = True
        
    
    # Screen-clearing code goes here. Don't put other drawing commands above this, or they will be erased with this command.
    screen.fill(BLACK)

    # Drawing code should go here
    

    # This counter will help us manipulate the frames better
    counter += 1
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
# ------------------------------------------------- GAME LOGIC & EVERYTHING ------------------------------------------ 
# Close the window and quit.
pygame.quit()
