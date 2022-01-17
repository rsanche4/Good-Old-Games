# ----------------------------------------------------------------
# RAF ENGINE: Rapid And Fun 
# By Rafael Sanchez
# Description: This is my own Game Engine for making Pygame games.
# ----------------------------------------------------------------
# Code is devided in sections
# ------------------------------------------------- ESSENTIALS ------------------------------------------------------- 
# Imports go here
import pygame
from pygame import mixer

# Here import the buttons that you want from pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_SPACE,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

# Insert Game Title
GAME_TITLE = "RAF ENGINE"

# Here initialize the game. Leave this alone.
pygame.init()
pygame.font.init()
mixer.init()

# Change game Icon for window
# programIcon = pygame.image.load('Data\ikon.png')
# pygame.display.set_icon(programIcon)

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
# FONT = pygame.font.Font('Data\font.otf', 100)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# ------------------------------------------------- ESSENTIALS ------------------------------------------------------- 
# ------------------------------------------------- USEFUL -----------------------------------------------------------
# Define variables for game logic here 
PLAYER_W = 60
PLAYER_H = 60
player_x = WID//2
player_y = HEI//2

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
def dummy_func():
    pass

# Objects, Classes, Players, Enemies, everything of that sort
class RafObject:
    def __init__(self, x, y, w, h):
        self.width = w
        self.height = h
        self.location_x = x
        self.location_y = y
        
    def update(self, x, y):
        pygame.draw.rect(screen, WHITE, (x, y, self.width, self.height))

# Initialize other varibles, classes (Optional)
rObj = RafObject(player_x, player_y, PLAYER_W, PLAYER_H)
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
    if keys[K_LEFT] and x > 0:
        pass
    if keys[K_RIGHT] and x < (WID-PLAYER_W):
        pass
    if keys[K_UP] and y > 50:
        pass
    if keys[K_DOWN] and y < (HEI-PLAYER_H):
        pass
    if keys[K_SPACE]:
        pass
    if keys[K_RETURN]:
        pass
    if keys[K_ESCAPE]:
        pass
        
    # Screen-clearing code goes here. Don't put other drawing commands above this, or they will be erased with this command.
    screen.fill(BLACK)
 
    # Drawing code should go here
    # bg_img = pygame.image.load("bg_vg.bmp")
    # bg_rect = bg_img.get_rect()
    # screen.blit(bg_img, bg_rect)
    # text = FONT.render('PRESS ENTER TO PLAY AGAIN', True, GREEN)
    # textRect = text.get_rect()
    # textRect.topleft = (WID//2-textRect.width//2, HEI//2-textRect.width//2+270)
    # screen.blit(text, textRect)
    rObj.update(WID//2, HEI//2)

    # This counter will help us manipulate the frames better
    counter += 1
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
# ------------------------------------------------- GAME LOGIC & EVERYTHING ------------------------------------------ 
# Close the window and quit.
pygame.quit()
