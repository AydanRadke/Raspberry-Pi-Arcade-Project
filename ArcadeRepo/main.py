'''This was made to familiarize myself with pygame. 
I followed this guide: https://coderslegacy.com/python/pygame-platformer-game-development'''

import pygame
from pygame.locals import *
import random
import sys

# Pygame initialization and important constants
pygame.init()
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

frames_per_sec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# player class. Creates a 2d surface, gives it color, and places it. Docs for surfaces can be found here: https://www.pygame.org/docs/ref/surface.html
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10, 420))

        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    # This handles the player movement. Great resource for later on!!
    def move(self):
        # This second value sets gravity. x acceleration is the first value, then y acceleration. Remember positive y direction is down
        self.acc = vec(0,0.5)

        # Decide acceleration
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        
        # We're effectively subtracting velocity times friction from the current acceleration.
        self.acc.x += self.vel.x * FRIC
        # We add the acceleration to the velocity
        self.vel += self.acc
        # Update the position. Not sure why we add half of the acceleration though? Maybe I'll ask chatgpt
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

    def jump(self):
        # If the player is colliding with a sprite, let them jump
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15
        self.move()
 
    def update(self):
        hits = pygame.sprite.spritecollide(player_one, platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
    

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Generates a surface of random size and location
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH-10), random.randint(0, HEIGHT-30)))

    def move(self):
        pass

def platform_generation():
    while len(platforms) < 7:
        width = random.randrange(50,100)
        p = platform()
        p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))

        platforms.add(p)
        all_sprites.add(p)

# Create sprites and then put them in a group. We group them so they can be updated later on in the game loop.
platform_one = platform()
platform_one.surf = pygame.Surface((WIDTH, 20))
platform_one.surf.fill((255,0,0))
platform_one.rect = platform_one.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
player_one = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(platform_one)
all_sprites.add(player_one)

# We create a different group of sprites for the platforms. This is so we can differentiate between player and platform sprites
# For the purposes of collision
platforms = pygame.sprite.Group()
platforms.add(platform_one)

# Generates platforms of the differing size and location
for x in range(random.randint(5, 6)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)

# main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            look_at_this = event
            if event.key == pygame.K_SPACE:
                # TODO Need to figure out why the jump method doesn't work. Maybe play with how pygame
                # pygame handles keypresses?
                player_one.jump()
    
    displaysurface.fill((0,0,0))
    player_one.update()

    for entity in all_sprites:
        entity.move()
        displaysurface.blit(entity.surf, entity.rect)
    
    platform_generation()

    if player_one.rect.top <= HEIGHT / 3:
        player_one.pos.y += abs(player_one.vel.y)
        for plat in platforms:
            plat.rect.y += abs(player_one.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    pygame.display.update()
    frames_per_sec.tick(FPS)

