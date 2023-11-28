#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

from gobject import *
from gresource import *

TITLE_STR = "Sprite Animation"

STATUS_XOFFSET = 10
STATUS_YOFFSET = 5

CHARACTER_SPEED = 5

MOVE_STOP = 0
MOVE_LEFT = 1
MOVE_RIGHT = 2

def terminate() :
    pygame.quit()
    sys.exit()

def run_game() :
    global background, character

    start_game()

    character.set_life_count(3)

    move = MOVE_STOP

    crashed = False
    while not crashed :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                crashed = True

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP:
                    character.set_speed(0, -1 * CHARACTER_SPEED)
                elif event.key == pygame.K_DOWN :
                    character.set_speed(0, CHARACTER_SPEED)
                elif event.key == pygame.K_F10 :
                    gctrl.save_scr_capture(TITLE_STR)

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                    character.set_speed(0, 0)
                elif event.key == pygame.K_LEFT :
                    move = MOVE_LEFT
                elif event.key == pygame.K_RIGHT :
                    move = MOVE_RIGHT
                elif event.key == pygame.K_SPACE :
                    move = MOVE_STOP

        # Update character
        character.move()

        # Clear surface
        gctrl.surface.fill(COLOR_WHITE)

        # Draw background
        if move == MOVE_RIGHT :
            background.scroll_left()
            background.draw()

            character.draw_sprite('right', 0)            
        elif move == MOVE_LEFT :
            background.scroll_right()
            background.draw()

            character.draw_sprite('left', 0)
        elif move == MOVE_STOP :
            background.draw()
            character.draw()

        pygame.display.update()
        gctrl.clock.tick(FPS)
        
    terminate()

def start_game() :
    # Clear surface
    gctrl.surface.fill(COLOR_WHITE)

    gctrl.draw_string(TITLE_STR, 0, 0, ALIGN_CENTER, 60, COLOR_BLACK)
    gctrl.draw_string("press any key", 0, 100, ALIGN_CENTER | ALIGN_BOTTOM, 30, COLOR_RED)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        gctrl.clock.tick(FPS)    
       
def init_game() :
    global background, character
  
    # backgroud and screen
    background = backgroud_object('id_background')
    pad_width = background.width
    pad_height = background.height

    gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
    pygame.display.set_caption(TITLE_STR)

    # character
    character = game_object(pad_width / 2 - 10, pad_height - 150, 'id_character')
    character.add_sprite('left', sprite_left)
    character.add_sprite('right', sprite_right)

if __name__ == '__main__' :
    init_game()
    run_game()

