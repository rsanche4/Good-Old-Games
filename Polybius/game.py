# ----------------------------------------------------------------
# POLYBIUS
# By Rafael Sanchez
# Description: A clone of the classic myth.
# ----------------------------------------------------------------
# Code is devided in sections
# ------------------------------------------------- ESSENTIALS ------------------------------------------------------- 
# Imports go here
import pygame
from pygame import mixer
import random

# Here import the buttons that you want from pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_ESCAPE,
    QUIT,
)

# Insert Game Title
GAME_TITLE = "POLYBIUS"

# Here initialize the game. Leave this alone.
pygame.init()
pygame.font.init()
mixer.init()

# Change game Icon for window
programIcon = pygame.image.load('Data\\ikon.png')
pygame.display.set_icon(programIcon)

# Define some playtesting colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define size of Game Window
WID = 255*2
HEI = 302*2

# Width and Height of the screen are initialized
size = (WID, HEI)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN|pygame.SCALED)

# Display Game Title
pygame.display.set_caption(GAME_TITLE)

# Define the fonts to be used in-game
F = 'Data\\Polybius1981.ttf'
MAX_SIZE = 100
SIZES = [int(MAX_SIZE*0.2), int(MAX_SIZE*0.4), int(MAX_SIZE*0.6), int(MAX_SIZE*0.8), MAX_SIZE]

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# ------------------------------------------------- ESSENTIALS ------------------------------------------------------- 
# ------------------------------------------------- USEFUL -----------------------------------------------------------
# Define variables for game logic here 
player_x = WID//2
player_y = 70
is_menu = True
game_mode = False
direction = 0
level = 0
score = 0
MAX_LIF = 7
lif = 0
big_number = 0
middles = ['Data\\middle.png', 'Data\\middle2.png', 'Data\\middle3.png', 'Data\\middle4.png', 'Data\\middle5.png', 'Data\\middle6.png']
numbers = [35, 50, 75, 85, 90, 100, 115]
circ_r = 1
circ_t = 1
PLAYER_W = 0
PLAYER_H = 0
rand = 5
rloc = -1
en_vel = 0
init_timeout = True
timeout = 4000
cur_time = 0

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

def level_aesth(level, counter, middleCirc):
    global circ_r
    global circ_t
    color = (0, 0, 0)
    if level == 0:
        if counter % 50 != 0:
            circ_r += 10 
        else:
            circ_r = 1
            circ_t = 15
        color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    if level == 1:
        if counter % 100 != 0:
            circ_r += 5 
        else:
            circ_r = 1
            circ_t = 100
        color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    if level == 2:
        if counter % 10 != 0:
            circ_r += 70 
        else:
            circ_r = 1
            circ_t = 5
        color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    if level == 3:
        if counter % 500 != 0:
            circ_r += 1 
        else:
            circ_r = 1
            circ_t = 100
        color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    if level == 4:
        if counter % 50 != 0:
            circ_r += 10 
        else:
            circ_r = 1
            circ_t = 15
        if counter % 50 < 25:
            color = RED
        else:
            color = BLUE
    if level == 5:
        if counter % 50 != 0:
            circ_r += 10 
        else:
            circ_r = 1
            circ_t = 15
        if counter % 50 < 25:
            color = BLUE
        else:
            color = RED
    if level == 6:
        if counter % 100 != 0:
            circ_r += 5 
        else:
            circ_r = 1
            circ_t = 100
        if counter % 300 < 100:
            color = GREEN
        elif counter % 300 < 200:
            color = BLUE
        else:
            color = RED
    if level == 7:
        if counter % 500 != 0:
            circ_r += 1 
        else:
            circ_r = 1
            circ_t = 200
        color = (random.randint(80,110),0,0)
    middleCirc.update(circ_r, circ_t, color)

def messages(counter, rand):
    if counter % 100 == 0:
        if rand == 1:
            font_master(F, SIZES[4], 'OBEY', False, WHITE, True, 0, 70)
        if rand == 2:
            font_master(F, SIZES[4], 'CONFORM', False, WHITE, True, 0, 0)
        if rand == 3:
            font_master(F, SIZES[4], 'CONSUME', False, WHITE, True, 0, 0)
        if rand == 4:
            font_master(F, SIZES[4], 'BUY', False, WHITE, True, 0, 70)
        if rand == 5:
            font_master(F, SIZES[3], 'LOSE YOURSELF', False, WHITE, True, 0, 200)
        if rand == 6:
            font_master(F, SIZES[4], 'SUBMIT', False, WHITE, True, 0, 0)

# Objects, Classes, Players, Enemies, everything of that sort
class Player:
    def __init__(self, x, y):
        global PLAYER_W
        global PLAYER_H
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Data\\player1.png').convert_alpha()
        self.rect = self.image.get_rect()
        PLAYER_H = self.rect.height
        PLAYER_W = self.rect.width
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def update(self, dir):
        global player_x
        global player_y
        if dir % 8 == 7:
            self.image = pygame.image.load('Data\\player7.png').convert_alpha()
            self.x = ((WID//2)//2)
            self.y = ((HEI//2)//2)
        if dir % 8 == 6:
            self.image = pygame.image.load('Data\\player1.png').convert_alpha()
            self.x = WID//2
            self.y = 70
        if dir % 8 == 5:
            self.image = pygame.image.load('Data\\player8.png').convert_alpha()
            self.x = (WID//2)+((WID//2)//2)
            self.y = ((HEI//2)//2)
        if dir % 8 == 4:
            self.image = pygame.image.load('Data\\player4.png').convert_alpha()
            self.x = WID-50
            self.y = HEI//2
        if dir % 8 == 3:
            self.image = pygame.image.load('Data\\player5.png').convert_alpha()
            self.x = (WID//2)+((WID//2)//2)
            self.y = (HEI//2)+((HEI//2)//2)
        if dir % 8 == 2:
            self.image = pygame.image.load('Data\\player2.png').convert_alpha()
            self.x = WID//2
            self.y = HEI-70
        if dir % 8 == 1:
            self.image = pygame.image.load('Data\\player6.png').convert_alpha()
            self.x = ((WID//2)//2)
            self.y = (HEI//2)+((HEI//2)//2)
        if dir % 8 == 0:
            self.image = pygame.image.load('Data\\player3.png').convert_alpha()
            self.x = 50
            self.y = HEI//2
        player_x = self.x
        player_y = self.y
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

class Enemy:
    def __init__(self, x, y, number):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.number = number
        self.image = 0
    
    def update(self, direction, make_inv, vel):
        global WID
        global HEI
        global lif
        global big_number
        global level
        global score
        global numbers
        if make_inv:
            self.image = pygame.image.load('Data\\empty.png').convert_alpha()
        else:
            if self.number == 0:
                self.image = pygame.image.load('Data\\enull.png').convert_alpha()
            elif self.number == 5:
                self.image = pygame.image.load('Data\\e5.png').convert_alpha()
            elif self.number == 10:
                self.image = pygame.image.load('Data\\e10.png').convert_alpha()
            elif self.number == 25:
                self.image = pygame.image.load('Data\\e25.png').convert_alpha()
            elif self.number == 50:
                self.image = pygame.image.load('Data\\e50.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        if direction == -1:
            self.x = WID//2
            self.y = HEI//2
        elif direction == 0:
            self.x = WID//2
            self.y -= vel
        elif direction == 1:
            self.x -= vel
            self.y -= vel
        elif direction == 2:
            self.x -= vel
            self.y = HEI//2
        elif direction == 3:
            self.x -= vel
            self.y += vel
        elif direction == 4:
            self.x = WID//2
            self.y += vel
        elif direction == 5:
            self.x += vel
            self.y += vel
        elif direction == 6:
            self.x += vel
            self.y = HEI//2
        elif direction == 7:
            self.x += vel
            self.y -= vel        
        if abs(player_x - self.x) < self.width and abs(player_y - self.y) < self.height:
            self.x = -1000
            self.y = -1000
            if self.number == 0:
                lif -= 1
                throwaway = sound_master('Data\\attack.mp3', False, False)
            else:
                temp1 = big_number
                big_number -= self.number
                if big_number < 0:
                    lif -= 1
                    throwaway = sound_master('Data\\attack.mp3', False, False)
                    big_number = temp1
                elif big_number == 0:
                    score += 10
                    big_number = numbers[random.randint(0, 6)]
                    level = random.randint(0, 7)
                    throwaway1 = sound_master('Data\\level_up.mp3', False, False)
                else:
                    throwaway = sound_master('Data\\scoreplus.mp3', False, False)            
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, r, t, rgb):
        pygame.draw.circle(screen, rgb, (self.x, self.y), r, t)

# Initialize other varibles, classes (Optional)
p = Player(player_x, player_y)
middleCirc = Circle(WID//2, HEI//2)
en1 = Enemy(WID//2, HEI//2, 0)
en2 = Enemy(WID//2, HEI//2, 0)
en3 = Enemy(WID//2, HEI//2, 0)
en4 = Enemy(WID//2, HEI//2, 0)
en5 = Enemy(WID//2, HEI//2, 0)
en6 = Enemy(WID//2, HEI//2, 0)
en7 = Enemy(WID//2, HEI//2, 5)
en8 = Enemy(WID//2, HEI//2, 10)
en9 = Enemy(WID//2, HEI//2, 25)
en10 = Enemy(WID//2, HEI//2, 50)
en_arr = [0, en1, en2, en3, en4, en5, en6, en7, en8, en9, en10]
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
        if keys[K_LEFT] and not is_menu and game_mode:
            direction -= 1
        if keys[K_RIGHT] and not is_menu and game_mode:
            direction += 1
        if keys[K_RETURN] and is_menu and not game_mode:
            is_menu = False
            game_mode = True
            score = 0
            level = random.randint(0, 7)
            big_number = numbers[random.randint(0, 6)]
            direction = 0
            lif = MAX_LIF
            rand = 5
            rloc = -1
            en_vel = 0
            throwaway = sound_master('Data\\game_ost.mp3', True, True)
            throwaway1 = sound_master('Data\\coins.mp3', False, False)
        elif keys[K_RETURN] and not is_menu and not game_mode:
            mixer.music.stop()
            level = 0
            is_menu = True
            game_mode = False
        if keys[K_ESCAPE] and is_menu:
            done = True
        
    
    # Screen-clearing code goes here. Don't put other drawing commands above this, or they will be erased with this command.
    if level == 6:
        screen.fill((random.randint(0,50),random.randint(0,50),random.randint(0,50)))    
    else:
        screen.fill((0,0,20))

    # Drawing code should go here
    if is_menu:
        image = pygame.image.load('Data\\title3.png').convert_alpha()
        rect = image.get_rect()
        rect.center = (WID//2, 170)
        screen.blit(image, rect)
        font_master(F, SIZES[1], '(c) 1981 Sinneslöschen Inc.', False, BLUE, True, 0, 290)
        font = pygame.font.Font(F, SIZES[1])
        text = font.render('Credits 1', False, RED)
        textRect = text.get_rect()
        font_master(F, SIZES[1], 'Credits 0', False, RED, False, (WID//2)-(textRect.width//2), 490)
    elif game_mode:
        level_aesth(level, counter, middleCirc)        
        image = pygame.image.load(middles[(counter%12)//2]).convert_alpha()
        rect = image.get_rect()
        rect.center = (WID//2, HEI//2)
        screen.blit(image, rect)        
        p.update(direction)
        if counter % 100 < 50:
            if counter % 100 == 0:
                temp = rand
                if temp == 10:
                    rand = random.randint(1, 9)
                elif temp == 1:
                    rand = random.randint(2, 10)
                else:
                    a = [random.randint(1, temp-1),random.randint(temp+1, 10)]
                    rand = a[random.randint(0, 1)]
                en_vel = 5
                rloc = random.randint(0, 7)
            for i in range(1, len(en_arr)):
                if i == rand:
                    en_arr[rand].update(rloc, False, en_vel)
                else:
                    en_arr[i].update(-1, True, en_vel)
        if lif <= 0:
            game_mode = False
        font_master(F, SIZES[1], str(score), False, RED, False, 15, HEI-45)
        image = pygame.image.load('Data\\live.png').convert_alpha()
        rect = image.get_rect()
        for i in range(0, lif):
            rect.center = (WID-20-(i*10), HEI-25)
            screen.blit(image, rect)
        font_master(F, SIZES[1], str(big_number), False, GREEN, False, WID//2-25, 10)
        if counter % 700 == 0:
            messages(counter, random.randint(1, 6))
    else:
        mixer.music.stop()
        level = 6
        font_master(F, SIZES[4], 'GAME OVER', False, GREEN, True, 0, 55)
        font_master(F, SIZES[2], 'INSERT CREDIT', False, GREEN, True, 0, 300)
        font_master(F, SIZES[2], str(score), False, RED, False, WID//2-10, HEI//2+40)
        if init_timeout:
            cur_time = counter
            init_timeout = False
        elif counter-cur_time >= timeout:
            level = 0
            cur_time = 0
            is_menu = True
            init_timeout = True
            game_mode = False

    # This counter will help us manipulate the frames better
    counter += 1
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
# ------------------------------------------------- GAME LOGIC & EVERYTHING ------------------------------------------ 
# Close the window and quit.
pygame.quit()
