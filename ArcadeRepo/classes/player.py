import pygame
from pygame.locals import *
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

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.dashing = False
    
    # Figure out how tf to do this. Should I set these as parameters?? idk
    def move(self, ACC, delta_time, FRIC, all_sprites, walls):
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

        # TODO The problem here is that the up and down directions take collision priority over left and right
        # if you're colliding with a wall on the right or left, and move up it detects it as a up and down
        # collision, simply because of the if elif order. Maybe find a way to fix it
        # Idea, set a tolerance. math.abs(self.rect.bottom - wall.rect.top > tolerance)
        # Because while colliding right or left it overlaps, and if you move up then it passes the up and down
        # collision check.
        # Might need to only add a tolerance statement to the up and down checks, because the left and right
        # don't misfire.
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
        
    def dash(self):
        if not self.dashing:
            self.vel *= 8