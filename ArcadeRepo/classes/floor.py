'''This is our floor class!As of right now this seems exactly like the wall class, but these will 
differ down the road because they will have different rules for how they look and behave.'''

import pygame
from pygame.locals import *

vec = pygame.math.Vector2

class Floor(pygame.sprite.Sprite):
    def __init__(self, image, FLOOR_WIDTH, FLOOR_HEIGHT, x, y):
            super().__init__()
            image = pygame.transform.scale(image, (FLOOR_WIDTH, FLOOR_HEIGHT))
            self.surf = image
            self.rect = self.surf.get_rect()

            self.pos = vec((x, y))

            self.rect.topleft = self.pos
        
    def move(self, ACC, delta_time, FRIC, all_sprites):
        self.rect.topleft = self.pos