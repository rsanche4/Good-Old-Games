# ---------------------------------------
# Blot Dodge
# @RSANCHE4
# ---------------------------------------

import pygame
import random
from pygame import mixer

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.font.init()
mixer.init()

# Change game Icon
programIcon = pygame.image.load('ikon.png')

pygame.display.set_icon(programIcon)

# Define some Globals
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

WID = 600
HEI = 800

PLAYER_W = 60
PLAYER_H = 60

BIG_FONT = pygame.font.Font('wheaton_capitals.otf', 100)
FONT = pygame.font.Font('wheaton_capitals.otf', 48)
SMALL_FONT = pygame.font.Font('wheaton_capitals.otf', 26)
SMALLEST_FONT = pygame.font.Font('wheaton_capitals.otf', 15)

is_menu = True
x = WID//2
y = HEI//2
vel = 10
scr = 0
lif = 3

# Set the width and height of the screen [width, height]
size = (WID, HEI)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("BLOT-DODGE")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def need_new_score():
    return (random.randint(50, WID-50), random.randint(50, HEI-50))

def color_changer(count):
    total = 255+255+255+255+255+255
    if count % total < 255:
        return (255, count % total, 0) 
    elif count % total < 255+255:
        return (255 - ((count % total) % 255), 255, 0)
    elif count % total < 255+255+255:
        return (0, 255, (count % total) % 255)
    elif count % total < 255+255+255+255:
        return (0,255 - ((count % total) % 255), 255)
    elif count % total < 255+255+255+255+255:
        return ((count % total) % 255, 0, 255)
    elif count % total < 255+255+255+255+255+255:
        return (255, 0, 255 - ((count % total) % 255))

# The enemies classes
class Horizontals_1:
    def __init__(self, rad, direction, speed):
        self.rad = rad
        self.direction = direction
        self.speed = speed
        if self.direction == 0:
            self.pos_x = -50
        else:
            self.pos_x = WID+50
        self.pos_y = random.randint(50, HEI-30)
        
    def update(self,player):
        if self.direction == 0:
            self.pos_x += self.speed
        else:
            self.pos_x -= self.speed
        pos = pygame.draw.circle(screen, BLACK, (self.pos_x, self.pos_y), self.rad)
        if (abs(pos.center[0] - player.center[0]) < self.rad+10 and abs(pos.center[1] - player.center[1]) < self.rad+10):
            global lif
            lif = lif - 1
            mixer.Sound('hit.wav').play()
            if self.direction == 0:
                self.pos_x = -50
            else:
                self.pos_x = WID+50
            self.pos_y = random.randint(50, HEI-30)
        elif self.direction == 0 and pos.center[0] > WID:
            self.pos_x = -50
            self.pos_y = random.randint(50, HEI-30)
        elif self.direction != 0 and self.pos_x < -50:
            self.pos_x = WID+50
            self.pos_y = random.randint(50, HEI-30)
    def restart(self):
        if self.direction == 0:
            self.pos_x = -50
        else:
            self.pos_x = WID+50
        self.pos_y = random.randint(50, HEI-30)
            

# -------- Main Program Loop -----------
counter = 0
alt = 0
init_scores = True
is_big_score = 0
score_loc = (0,0)
need_new_enemy = True
player = pygame.Rect(x, y, PLAYER_W, PLAYER_H)
game_over = False

a_1 = Horizontals_1(random.randint(30, 40),0,3)
b_1 = Horizontals_1(random.randint(30, 40),0,3)
a_2 = Horizontals_1(random.randint(30, 40),0,4)
b_2 = Horizontals_1(random.randint(30, 40),0,4)
a_3 = Horizontals_1(random.randint(30, 40),0,5)

a_10 = Horizontals_1(random.randint(30, 40),1,3)
b_10 = Horizontals_1(random.randint(30, 40),1,3)
a_20 = Horizontals_1(random.randint(30, 40),1,4)
b_20 = Horizontals_1(random.randint(30, 40),1,4)
a_30 = Horizontals_1(random.randint(30, 40),1,5)



while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
 
    # --- Game logic should go here
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and x > 0:
        x -= vel
    if keys[K_RIGHT] and x < WID-PLAYER_W:
        x += vel
    if keys[K_UP] and y > 50:
        y -= vel
    if keys[K_DOWN] and y < HEI-PLAYER_H:
        y += vel
    if keys[K_RETURN] and is_menu:
        is_menu = False
        mixer.Sound('enter.wav').play()
        music_number = random.randint(0,1)
        if music_number == 0: 
            mixer.music.load("trip.wav")
            mixer.music.set_volume(0.7)
            mixer.music.play(-1)
        elif music_number == 1:
            mixer.music.load("water.wav")
            mixer.music.set_volume(0.7)
            mixer.music.play(-1)
    if keys[K_RETURN] and game_over:
        game_over = False
        lif = 3
        scr = 0
        init_scores = True
        mixer.Sound('enter.wav').play()
        music_number = random.randint(0,1)
        if music_number == 0: 
            mixer.music.load("trip.wav")
            mixer.music.set_volume(0.7)
            mixer.music.play(-1)
        elif music_number == 1:
            mixer.music.load("water.wav")
            mixer.music.set_volume(0.7)
            mixer.music.play(-1)
        a_1.restart()
        b_1.restart()
        a_2.restart()
        b_2.restart()
        a_3.restart()
        a_10.restart()
        b_10.restart()
        a_20.restart()
        b_20.restart()
        a_30.restart()
    if keys[K_ESCAPE]:
        done = True
        
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
 
    # --- Drawing code should go here
    if is_menu:
        bg_img = pygame.image.load("bg_vg.bmp")
        bg_rect = bg_img.get_rect()
        screen.blit(bg_img, bg_rect)
        if counter % 5 == 0: 
            text_title = BIG_FONT.render('BLOT-DODGE', True, RED)
            textRect_title = text_title.get_rect()
            textRect_title.topleft = (WID//2-textRect_title.width//2, HEI//2-textRect_title.width//2+135)
            screen.blit(text_title, textRect_title)
        
        text = SMALL_FONT.render('PRESS ENTER TO START', True, GREEN)
        textRect = text.get_rect()
        textRect.topleft = (WID//2-textRect.width//2, HEI//2-textRect.width//2+250)
        screen.blit(text, textRect)

        text_q = SMALL_FONT.render('PRESS ESC TO QUIT', True, GREEN)
        textRect_q = text_q.get_rect()
        textRect_q.topleft = (WID//2-textRect_q.width//2, HEI//2-textRect_q.width//2+300)
        screen.blit(text_q, textRect_q)

        text_cred = SMALLEST_FONT.render('@2021  RSANCHE4', True, BLUE)
        textRect_cred = text_cred.get_rect()
        textRect_cred.topleft = (WID//2-textRect_cred.width//2, HEI//2-textRect_cred.width//2+320)
        screen.blit(text_cred, textRect_cred)

    elif game_over:
        mixer.music.stop()
        bg_img = pygame.image.load("bg_vg.bmp")
        bg_rect = bg_img.get_rect()
        screen.blit(bg_img, bg_rect)

        text_title = BIG_FONT.render('SCORE: ' + str(scr), True, BLUE)
        textRect_title = text_title.get_rect()
        textRect_title.topleft = (WID//2-textRect_title.width//2, HEI//2-textRect_title.width//2+100)
        screen.blit(text_title, textRect_title)

        text = SMALL_FONT.render('PRESS ENTER TO PLAY AGAIN', True, GREEN)
        textRect = text.get_rect()
        textRect.topleft = (WID//2-textRect.width//2, HEI//2-textRect.width//2+270)
        screen.blit(text, textRect)

        text_y = SMALL_FONT.render('OR ESC TO QUIT', True, GREEN)
        textRect_y = text_y.get_rect()
        textRect_y.topleft = (WID//2-textRect_y.width//2, HEI//2-textRect_y.width//2+320)
        screen.blit(text_y, textRect_y)
        
    else:
        screen.fill(color_changer(counter))
        player = pygame.Rect(x, y, PLAYER_W, PLAYER_H)
        pygame.draw.rect(screen, BLACK, player)
        if init_scores == True:
            score_loc = need_new_score()
            init_scores = False
            is_big_score = random.randint(0, 100)
        else:
            random_x = score_loc[0]
            random_y = score_loc[1]
            if is_big_score % 50 == 0:
                big_scr = pygame.Rect(random_x, random_y, 70, 70)
                pygame.draw.rect(screen, WHITE, big_scr, 20)
                if (abs(player.left - (random_x+70//2)) < 70 and abs(player.top - (random_y+70//2)) < 70):
                    mixer.Sound('collect.wav').play()
                    scr += 50
                    init_scores = True
            elif is_big_score % 10 == 0:
                pygame.draw.polygon(screen, WHITE, [(random_x,random_y),(random_x-40,random_y+40),(random_x+40,random_y+40)])
                if (abs(player.left+(PLAYER_W//2) - random_x) < 40 and abs(player.top+(PLAYER_H//2) - random_y) < 40) or \
               (abs(player.left+(PLAYER_W//2) - (random_x-20)) < 40 and abs(player.top+(PLAYER_H//2) - (random_y+20)) < 40) or \
               (abs(player.left+(PLAYER_W//2) - (random_x+20)) < 40 and abs(player.top+(PLAYER_H//2) - (random_y+20)) < 40):
                    mixer.Sound('collect-2.wav').play()
                    scr += 10
                    init_scores = True
            else:
                pygame.draw.polygon(screen, WHITE, [(random_x,random_y),(random_x-20,random_y+20),(random_x,random_y+40),(random_x+20,random_y+20)])
                if (abs(player.left+(PLAYER_W//2) - random_x) < 30 and abs(player.top+(PLAYER_H//2) - random_y) < 30) or \
               (abs(player.left+(PLAYER_W//2) - (random_x-20)) < 30 and abs(player.top+(PLAYER_H//2) - (random_y+20)) < 30) or \
               (abs(player.left+(PLAYER_W//2) - random_x) < 30 and abs(player.top+(PLAYER_H//2) - (random_y+40)) < 30) or \
               (abs(player.left+(PLAYER_W//2) - (random_x+20)) < 30 and abs(player.top+(PLAYER_H//2) - (random_y+20)) < 30):
                    mixer.Sound('collect-1.wav').play()
                    scr += 1
                    init_scores = True
        # enemies spawing
        a_1.update(player)
        b_1.update(player)
        a_2.update(player)
        b_2.update(player)
        a_3.update(player)
        a_10.update(player)
        b_10.update(player)
        a_20.update(player)
        b_20.update(player)
        a_30.update(player)
            
        text = FONT.render('SCORE: ' + str(scr), True, BLACK)
        textRect = text.get_rect()
        textRect.topleft = (0, 0)
        screen.blit(text, textRect)

        text_lif = FONT.render('HITS: ' + str(lif), True, BLACK)
        textRect_lif = text_lif.get_rect()
        textRect_lif.topleft = (WID-textRect_lif.width, 0)
        screen.blit(text_lif, textRect_lif)

        if lif <= 0:
            game_over = True

    alt += 1
    if alt % 4 == 0:
        counter += 1
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
