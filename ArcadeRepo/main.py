import pygame
from pygame.locals import *
import sys
from classes.player import Player
from classes.wall import Wall
from classes.enemy import Enemy
import classes.bullet
from levelgen import *
import levelgen
import rooms.roomconfig as rc
import flows.aydanflow1
import ui

# Pygame initialization
pygame.init()
vec = pygame.math.Vector2

display_surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Connor Smells")

# Important constants initialization
WIDTH, HEIGHT = display_surface.get_size()
PLAYER_WIDTH = WIDTH * 0.05
PLAYER_HEIGHT = HEIGHT * 0.05
ACC = WIDTH * 0.04
FRIC = 0.2
FPS = 60

frames_per_sec = pygame.time.Clock()

# Sprite initialization

player_one = Player(PLAYER_HEIGHT, PLAYER_WIDTH, HEIGHT, WIDTH)
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
friendly_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
# all_sprites.add(player_one)

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

set_rooms = set(rooms)
rooms = list(set_rooms)

for x in floors:
    all_sprites.add(x)
for x in new_walls:
    all_sprites.add(x)
    walls.add(x)

# test enemies
'''minion = Enemy(WIDTH, HEIGHT, player_one, PLAYER_WIDTH, PLAYER_HEIGHT, "big", 3.5, 1)
enemy1 = Enemy(WIDTH, HEIGHT, player_one, PLAYER_WIDTH, PLAYER_HEIGHT, "small", 3.5, 1)
enemy2 = Enemy(WIDTH, HEIGHT, player_one, PLAYER_WIDTH, PLAYER_HEIGHT, "normal", 3.5, 1)
enemy3 = Enemy(WIDTH, HEIGHT, player_one, PLAYER_WIDTH, PLAYER_HEIGHT, "normal", 3.5, 1)
all_sprites.add(minion)
all_sprites.add(enemy1)
all_sprites.add(enemy2)
all_sprites.add(enemy3)
enemies.add(minion)
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)'''

in_room = False
temp_enemies = pygame.sprite.Group()

cur_health = player_one.health
hearts = ui.put_hearts_on_screen(cur_health, WIDTH, HEIGHT)
#for heart in hearts:
    #all_sprites.add(heart)
# initialize temp walls variable
temporary_walls = []

# main game loop!
while True:
    ''' Delta time is basically the change in time between frames.
    It will allow us to keep our changes consistent if the framerate ever changes'''
    # Handle inputs
    delta_time = frames_per_sec.get_time() / 1000
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_one.dash()
            if event.key == pygame.K_y:
                new_bullet = player_one.shoot(enemies)
                if new_bullet:
                    friendly_bullets.add(new_bullet)
                    all_sprites.add(new_bullet)
    

    # handle hearts TODO FIX FIX THIS PELASE GOD
    if player_one.health < cur_health:
        for heart in hearts:
            heart.kill()
        
        cur_health = player_one.health
        hearts = ui.put_hearts_on_screen(cur_health, WIDTH, HEIGHT)
    
    
    display_surface.fill((119, 112, 200))

    # Handle Bullets
    for bullet in friendly_bullets:
        delete_bullet = bullet.update(delta_time, enemies, walls)
        display_surface.blit(bullet.surf, bullet.rect)
        if delete_bullet:
            friendly_bullets.remove(bullet)

    for bullet in enemy_bullets:
        delete_bullet = bullet.update(delta_time, enemies, walls)
        display_surface.blit(bullet.surf, bullet.rect)
        if delete_bullet:
            friendly_bullets.remove(bullet)

    for entity in all_sprites:
        entity.move(ACC, delta_time, FRIC, all_sprites)
        display_surface.blit(entity.surf, entity.rect)
    
    # should throw in a check for the rooms
    '''1. Loop through a list of the rooms, checking if you're inside 2. if the room hasn't had its enemies defeated yet,
    toggle a boolean, close doors, spawn enemies 3. After the enemies are defeated, toggle a boolean, open doors, and 
    set up to check list of rooms again.'''
    if not in_room:
        for room in rooms:
            if WIDTH / 2 < room.bot_right[0] - 250 and WIDTH / 2 > room.top_left[0] + 250 and HEIGHT / 2 < room.bot_right[1] - 250 and HEIGHT / 2 > room.top_left[1] + 250 and room.room_type != "spawn" and not room.cleared:
                in_room = True
                room.cleared = True
                print(f"In room {rooms.index(room)}, type: {room.room_type}, {room.tiles}")
                temporary_walls = room.shut_room()
                for wall in temporary_walls:
                    all_sprites.add(wall)
                    walls.add(wall)
                new_enemies = room.start_fight(WIDTH, HEIGHT, player_one, PLAYER_WIDTH, PLAYER_HEIGHT)
                for enemy in new_enemies:
                    all_sprites.add(enemy)
                    enemies.add(enemy)
                    temp_enemies.add(enemy)
    elif len(temp_enemies) == 0 and room.room_type != 'spawn' and room.room_type != 'shop' and room.room_type != 'treasure':
                in_room = False
                for wall in temporary_walls:
                    wall.kill()
    



    # Need to add some sort of keydown sensor here for the player to be able to shoot.
    # Might need to grow into its own file because of how items affect shooting.
    for enemy in enemies:
        enemy.self_movement(ACC, delta_time, FRIC, all_sprites, walls)
        new_bullet = enemy.shoot(player_one, delta_time)
        if new_bullet:
            enemy_bullets.add(new_bullet)
            all_sprites.add(new_bullet)

    player_one.move(ACC, delta_time, FRIC, all_sprites, walls, rooms)

    for heart in hearts:
        heart.move(ACC, delta_time, FRIC, all_sprites)
        display_surface.blit(heart.surf, heart.rect)

    display_surface.blit(player_one.surf, player_one.rect)
    pygame.display.update()
    frames_per_sec.tick(FPS)