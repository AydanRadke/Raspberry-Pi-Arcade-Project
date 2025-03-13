import pygame
import random
import math
from .enemy_bullet import Enemy_Bullet

vec = pygame.math.Vector2
ACC = 0
'''
***Enemy Types***
- Big enemy with a lot of health, slowly/medium-slowly approaches the player but doesn't shoot.
- Average enemy, normal all stats
- Small fast enemy that shoot many bullets
'''

class Enemy(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT, player, player_width, player_height, type, switch_time, shoot_time, posx, posy, image=None):
        super().__init__()
        self.type = type
        self.player = player
        self.screen_width, self.screen_height = WIDTH, HEIGHT


        if image:
            self.surf = image
        elif type == "normal":
            self.surf = pygame.Surface((player_height, player_width))
            self.surf.fill((255, 0, 0))
            self.health = 200
            self.ACC = WIDTH * 0.05
            self.switch_time = 3.5
            self.shoot_time = 1
        elif type == "big":
            self.surf = pygame.Surface((player_height * 1.5, player_width * 1.5))
            self.surf.fill((0, 255, 0))
            self.health = 400
            self.ACC = WIDTH * 0.025
            self.switch_time = 1
            self.shoot_time = False
        elif type == "small":
            self.surf = pygame.Surface((player_height * 0.75, player_width * 0.75))
            self.surf.fill((125, 125, 0))
            self.health = 100
            self.ACC = WIDTH * 0.1
            self.switch_time = 3.5
            self.shoot_time = 0.5
            
        self.rect = self.surf.get_rect()
        # self.pos = vec((2 *(WIDTH / 3), 2 * (HEIGHT / 3)))
        self.pos = vec(posx, posy)
        self.vel = vec(0, 0)
        self.rect.center = self.pos
        self.time_left = switch_time  # Time before switching direction
        self.shoot_cooldown_left = shoot_time
        self.angle = self.new_angle()

        self.ACC = WIDTH * 0.05

    def move(self, ACC, delta_time, FRIC, all_sprites):
        self.rect.center = self.pos

    def self_movement(self, ACC, delta_time, FRIC, all_sprites, walls):
        speed = self.ACC * 1.3
        self.time_left -= delta_time
        if self.time_left <= 0:
            self.angle = self.new_angle()
            self.time_left = self.switch_time
        self.vel.x, self.vel.y = math.cos(self.angle) * speed * delta_time, math.sin(self.angle) * speed * delta_time

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                overlap_top = abs(self.rect.bottom - wall.rect.top)
                overlap_bottom = abs(self.rect.top - wall.rect.bottom)
                overlap_left = abs(self.rect.right - wall.rect.left)
                overlap_right = abs(self.rect.left - wall.rect.right)

                min_overlap = min(overlap_top, overlap_bottom, overlap_left, overlap_right)

                if min_overlap == overlap_top and self.vel.y > 0:
                    self.rect.bottom = wall.rect.top - 4
                    self.vel.y = 0
                elif min_overlap == overlap_bottom and self.vel.y < 0: 
                    self.rect.top = wall.rect.bottom + 4
                    self.vel.y = 0
                elif min_overlap == overlap_left and self.vel.x > 0:
                    self.rect.right = wall.rect.left - 4
                    self.vel.x = 0
                elif min_overlap == overlap_right and self.vel.x < 0:
                    self.rect.left = wall.rect.right + 4
                    self.vel.x = 0
            
        self.pos += self.vel
        self.rect.center = self.pos

        # check for contact damage

        if self.rect.colliderect(self.player.rect) and self.player.damage_cooldown_left <= 0 and self.player.dashing_cooldown_left <= 0.5:
            print("contact")
            self.player.damage_cooldown_left = self.player.damage_cooldown
            self.player.health -= 1
        '''if self.rect.top < wall.rect.bottom and self.vel.y < 0:
                    self.vel.y = 0
                    self.rect.top = wall.rect.bottom
                elif self.rect.bottom > wall.rect.top and self.vel.y > 0:
                    self.vel.y = 0
                    self.rect.bottom = wall.rect.top
                if self.rect.right > wall.rect.left and self.vel.x > 0:
                    self.vel.x = 0
                    self.rect.right = wall.rect.left
                elif self.rect.left < wall.rect.right and self.vel. x < 0:
                    self.vel.x = 0
                    self.rect.left = wall.rect.right
                self.pos = self.rect.center'''
        
    def shoot(self, player, delta_time):
        if self.shoot_time:
            self.shoot_cooldown_left -= delta_time
            if self.shoot_cooldown_left <= 0:
                speed = self.ACC * 4
                starting_position = self.rect.center
                new_bullet = Enemy_Bullet(speed, starting_position, player)
                self.shoot_cooldown_left = self.shoot_time
                return new_bullet
    
    def new_angle(self):
        if self.type == "big":
            print("trying to find the player") 
            print(f'Player pos {self.screen_width / 2}, {self.screen_width / 2}') # What the hell man
            return math.atan2(self.screen_height / 2 - self.pos.y, self.screen_width / 2 - self.pos.x)
        return random.uniform(0, 2 * math.pi)


