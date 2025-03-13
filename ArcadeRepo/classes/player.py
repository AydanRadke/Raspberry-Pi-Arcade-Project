import pygame
from pygame.locals import *
import math
from .bullet import Bullet
vec = pygame.math.Vector2
# TODO try to get this fixed lol
# This is our player class
screen_height = 0
screen_width = 0
class Player(pygame.sprite.Sprite):
    def __init__(self, PLAYER_HEIGHT, PLAYER_WIDTH, HEIGHT, WIDTH):
        screen_height = HEIGHT
        screen_width = WIDTH
        super().__init__()
        self.surf = pygame.Surface((PLAYER_HEIGHT, PLAYER_WIDTH))
        self.surf.fill((232, 130, 200))
        self.rect = self.surf.get_rect()
        self.pos = vec((WIDTH / 2, HEIGHT / 2))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 6

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.dashing = False
        self.acceleration_value = 0
        self.dashing_cooldown = 1.5
        self.dashing_cooldown_left = self.dashing_cooldown

        self.damage_cooldown = 1
        self.damage_cooldown_left = self.damage_cooldown

        self.shooting_cooldown_time = 0.5  # Shooting cooldown
        self.shooting_cooldown_left = self.shooting_cooldown_time  # Time before player can shoot again
        
    
    def move(self, ACC, delta_time, FRIC, all_sprites, walls, rooms):
        
        # subtract from damage cooldown
        self.damage_cooldown_left -= delta_time
        # if out of health, end game
        if self.health <= 0:
            self.kill()
            quit()

        self.dashing_cooldown_left -= delta_time
        self.shooting_cooldown_left -= delta_time
        self.acceleration_value = ACC
        self.acc = vec(0, 0)
        pressed_keys = pygame.key.get_pressed()

        # Decide acceleration based on key input
        if pressed_keys[K_w]:
            self.acc.y = -ACC * delta_time
        if pressed_keys[K_a]:
            self.acc.x = -ACC * delta_time
        if pressed_keys[K_s]:
            self.acc.y = ACC * delta_time
        if pressed_keys[K_d]:
            self.acc.x = ACC * delta_time

        # Apply friction
        self.acc += self.vel * -FRIC
        self.vel += self.acc

        for wall in walls:
            if self.rect.colliderect(wall.rect):  # Check if the player collides with a wall
                overlap_left = abs(self.rect.left - wall.rect.right)
                overlap_right = abs(self.rect.right - wall.rect.left)
                overlap_up = abs(self.rect.top - wall.rect.bottom)
                overlap_down = abs(self.rect.bottom - wall.rect.top)
            
                min_overlap = min(overlap_left, overlap_right, overlap_up, overlap_down)
                if overlap_left == min_overlap:
                    self.vel.x = 0
                    for entity in all_sprites:
                        entity.pos.x -= min_overlap
                if overlap_right == min_overlap:
                    self.vel.x = 0
                    for entity in all_sprites:
                        entity.pos.x += overlap_right
                if overlap_up == min_overlap:
                    self.vel.y = 0
                    for entity in all_sprites:
                        entity.pos.y -= overlap_up
                if overlap_down == min_overlap:
                    self.vel.y = 0
                    for entity in all_sprites:
                        entity.pos.y += overlap_down
                    
            # Previous solution to collision
            '''
                if self.rect.bottom > wall.rect.top or self.rect.top < wall.rect.bottom:
                    if self.rect.bottom > wall.rect.top:  # Bottom edge of player collides with top edge of wall
                        if self.vel.y > 0:
                            self.vel.y = -1  # Stop vertical velocity

                            y_difference = self.rect.bottom - wall.rect.top
                            for entity in all_sprites:
                                entity.pos.y += y_difference
                    if self.rect.top < wall.rect.bottom:  # Top edge of player collides with bottom edge of wall
                        if self.vel.y < 0:
                            self.vel.y = 1  # Stop vertical velocity
                            
                            y_difference = wall.rect.bottom - self.rect.top
                            for entity in all_sprites:
                                entity.pos.y += -y_difference
                elif self.rect.left < wall.rect.left or self.rect.right > wall.rect.left:
                    if self.rect.right > wall.rect.left:  # Right edge of player collides with left edge of wall
                        if self.vel.x > 0:
                            self.vel.x = -1  # Stop horizontal velocity

                            x_difference = self.rect.right - wall.rect.left
                            for entity in all_sprites:
                                entity.pos.x += x_difference
                    if self.rect.left < wall.rect.right:  # Left edge of player collides with right edge of wall
                        if self.vel.x < 0:
                            self.vel.x = 1

                            x_difference = wall.rect.right - self.rect.left
                            for entity in all_sprites:
                                entity.pos.x += -x_difference'''
        

        self.pos = vec((screen_width / 2, screen_height / 2))
        # moves all other sprites based on the velocity of the player
        for entity in all_sprites:
            entity.pos += -self.vel
        
        for room in rooms:
            room.bot_right[0] += -self.vel.x
            room.bot_right[1] += -self.vel.y
            room.top_left[0] += -self.vel.x
            room.top_left[1] += -self.vel.y
    
    def shoot(self, enemies):
        if self.shooting_cooldown_left <= 0:
            speed = self.acceleration_value * 6
            starting_position = self.rect.center
            new_bullet = Bullet(speed, starting_position, enemies, self.vel.normalize()) # TODO NOT IMPORTING RIGHT
            self.shooting_cooldown_left = self.shooting_cooldown_time
            return new_bullet
        
        return None

        
    def dash(self):
        if self.dashing_cooldown_left <= 0:
            if not self.dashing:
                self.vel *= 8
            self.dashing_cooldown_left = self.dashing_cooldown