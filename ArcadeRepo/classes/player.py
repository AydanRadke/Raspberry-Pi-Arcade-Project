import pygame
from pygame.locals import *
vec = pygame.math.Vector2
# TODO try to get this fixed lol
# This is our player class
class Player(pygame.sprite.Sprite):
    def __init__(self, PLAYER_HEIGHT, PLAYER_WIDTH, HEIGHT, WIDTH):
        super().__init__()
        self.surf = pygame.Surface((PLAYER_HEIGHT, PLAYER_WIDTH))
        self.surf.fill((232, 130, 200))
        self.rect = self.surf.get_rect()
        self.pos = vec((WIDTH / 2, HEIGHT / 2))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.dashing = False
    
    # Figure out how tf to do this. Should I set these as parameters?? idk
    def move(self, ACC, delta_time, FRIC, all_sprites):
        self.acc = vec(0,0)
        pressed_keys = pygame.key.get_pressed()
        # Decide acceleration
        if pressed_keys[K_w]:
            self.acc.y = -ACC * delta_time
        if pressed_keys[K_a]:
            self.acc.x = -ACC * delta_time
        if pressed_keys[K_s]:
            self.acc.y = ACC * delta_time
        if pressed_keys[K_d]:
            self.acc.x = ACC * delta_time
        
        self.acc += self.vel * -FRIC
        self.vel += self.acc
        # self.pos += self.vel

        # moves all other sprites based on the velocity of the player
        for entity in all_sprites:
            entity.pos += -self.vel
        
    def dash(self):
        if not self.dashing:
            self.vel *= 8