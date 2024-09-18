import pygame
from pygame.locals import *
import sys
from classes.player import Player
from classes.wall import Wall
from classes.enemy import Enemy

# Pygame initialization
pygame.init()
vec = pygame.math.Vector2

display_surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Connor Smells")

# Important constants initialization
WIDTH, HEIGHT = display_surface.get_size()
PLAYER_WIDTH = WIDTH * 0.05
PLAYER_HEIGHT = HEIGHT * 0.05
ACC = WIDTH * 0.05
FRIC = 0.2
FPS = 60

minion_image = pygame.image.load('ArcadeRepo/assets/mimion.png')

frames_per_sec = pygame.time.Clock()

# Sprite initialization
# TODO try to get the player.py class to work
player_one = Player(PLAYER_HEIGHT, PLAYER_WIDTH, HEIGHT, WIDTH)
random_wall = Wall(pygame.image.load('ArcadeRepo/assets/woodenwall.jpg'), 300, 300, WIDTH, HEIGHT)
minion = Enemy(minion_image, WIDTH, HEIGHT)
all_sprites = pygame.sprite.Group()
# all_sprites.add(player_one)
all_sprites.add(random_wall)
all_sprites.add(minion)

# main game loop!
while True:
    ''' I'll explain what delta time is right here. Basically, it's the change in time between frames.
    It will allow us to keep our changes consistent if the framerate ever changes'''
    delta_time = frames_per_sec.get_time() / 1000
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_one.dash()
    
    display_surface.fill((0,0,0))

    player_one.move(ACC, delta_time, FRIC, all_sprites)
    display_surface.blit(player_one.surf, player_one.rect)
    for entity in all_sprites:
        entity.move(ACC, delta_time, FRIC, all_sprites)
        display_surface.blit(entity.surf, entity.rect)

    pygame.display.update()
    frames_per_sec.tick(FPS)