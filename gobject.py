#!/usr/bin/python

import sys
import pygame
import random
import time

from gresource import *

class sprite_object :
    def __init__(self) :
        self.width = 0
        self.height = 0
        self.images = []
        self.cur_index = 0
    
    def draw(self, x, y) :
        image = self.images[self.cur_index]
        gctrl.surface.blit(image, (x, y))

        if self.cur_index < len(self.images) - 1 :
            self.cur_index += 1
        else : 
            self.cur_index = 0

class game_object :
    def __init__(self, x, y, resource_id) :
        if resource_id != None :
            resource_path = get_img_resource(resource_id)
            self.object = pygame.image.load(resource_path)
            self.width = self.object.get_width()
            self.height = self.object.get_height()
        else :
            self.object = None
            self.width = 0
            self.height = 0

        self.sprites = {}

        self.set_position(x, y)

        self.dx = 0
        self.dy = 0
        self.life_count = 1

    def add_sprite(self, key, sprite_src) :
        sprite = sprite_object()
        for image_path in sprite_src :
            sprite.images.append(pygame.image.load(image_path))

        sprite.width = sprite.images[0].get_width()
        sprite.height = sprite.images[0].get_height()

        self.sprites[key] = sprite

        print(self.sprites[key])

    def set_position(self, x, y) : 
        self.x = x
        self.y = y        
        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1
        
    def set_speed(self, del_x, del_y) :
        self.dx = del_x
        self.dy = del_y

    def move(self, del_x = 0, del_y = 0) :
        if del_x == 0 :
            del_x = self.dx
        if del_y == 0 :
            del_y = self.dy

        self.x += del_x
        self.y += del_y

        if self.y < 0 :
            self.y = 0
        elif self.y > (gctrl.height - self.height) :
            self.y = (gctrl.height - self.height)

        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def draw(self) :
        if self.object != None :
            gctrl.surface.blit(self.object, (self.x, self.y))            

    def draw_sprite(self, key, index) :
        if key in self.sprites :
            self.sprites[key].draw(self.x, self.y)  

    def is_out_of_range(self) :
        if self.x <= 0 or self.x >= gctrl.width :
            return True
        else :
            return False

    def is_life(self) :
        if self.life_count > 0 :
            return True
        else :
            return False
    
    def set_life_count(self, count) :
        self.life_count = count
        if self.life_count > 0 :
            self.life = True

    def get_life_count(self) :
        return self.life_count
    
    def kill_life(self) :
        self.life_count -= 1
        if self.life_count == 0 :
            self.life = False
            return False
        else :
            return True

    def check_crash(self, enemy_item, sound_object) :
        if self.object != None and enemy_item.object != None :
            if self.ex > enemy_item.x :
                if (self.y > enemy_item.y and self.y < enemy_item.ey) or (self.ey > enemy_item.y and self.ey < enemy_item.ey) :
                    #print("crashed1 : ",  self.x, self.y, self.ex, self.ey)
                    #print("crashed2 : ",  enemy_item.x, enemy_item.y, enemy_item.ex, enemy_item.ey)
                    if sound_object != None :
                        sound_object.play()
                    return True
        return False

class backgroud_object(game_object) :
    def __init__(self, resource_id) :
        resource_path = get_img_resource(resource_id)
        self.object = pygame.image.load(resource_path)
        self.object2 = self.object.copy()

        self.width = self.object.get_width()
        self.height = self.object.get_height()

        self.x = 0
        self.x2 = self.width
        self.scroll_width = -2

    def scroll_left(self) :
        self.x += self.scroll_width
        self.x2 += self.scroll_width

        if self.x == -self.width:
            self.x = self.width

        if self.x2 == -self.width:
            self.x2 = self.width

    def scroll_right(self) :
        if self.x == self.width:
            self.x = -self.width

        if self.x2 == self.width:
            self.x2 = -self.width

        self.x -= self.scroll_width
        self.x2 -= self.scroll_width

    def draw(self) :
        gctrl.surface.blit(self.object, (self.x, 0))
        gctrl.surface.blit(self.object2, (self.x2, 0))

if __name__ == '__main__' :
    print('game object')