import pygame
from pygame.locals import *
import sys
from classes.player import Player
from classes.wall import Wall
from classes.enemy import Enemy
from levelgen import *
import levelgen
import rooms.roomconfig as rc
import flows.aydanflow1

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

player_one = Player(PLAYER_HEIGHT, PLAYER_WIDTH, HEIGHT, WIDTH)
random_wall = Wall(pygame.image.load('ArcadeRepo/assets/woodenwall.jpg'), 300, 300, WIDTH, HEIGHT)
minion = Enemy(minion_image, WIDTH, HEIGHT)
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
# all_sprites.add(player_one)
all_sprites.add(random_wall)
all_sprites.add(minion)

# Room creation test
""" test_blueprint = Blueprint(rc.config['spawn']['aydanspawn1'])
test_room = Room(len(test_blueprint.layout[0]), len(test_blueprint.layout))
test_blueprint.apply(test_room)
walls, floors = test_room.create_room(100, 100)

for x in floors:
    all_sprites.add(x)
for x in walls:
    all_sprites.add(x)"""

rooms, new_walls, floors, parent = flows.aydanflow1.aydanflow1.draw_level(start_x=100, start_y=100)

for x in floors:
    all_sprites.add(x)
for x in new_walls:
    all_sprites.add(x)
    walls.add(x)

# main game loop!
while True:
    ''' Delta time is basically the change in time between frames.
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

    for entity in all_sprites:
        entity.move(ACC, delta_time, FRIC, all_sprites)
        display_surface.blit(entity.surf, entity.rect)

    player_one.move(ACC, delta_time, FRIC, all_sprites, walls)
    display_surface.blit(player_one.surf, player_one.rect)
    pygame.display.update()
    frames_per_sec.tick(FPS)