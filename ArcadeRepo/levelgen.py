import pygame
from pygame.locals import *
from classes.wall import Wall
from classes.floor import Floor
from classes.enemy import Enemy
import random
import math
import classes.spritesheet as spritesheet

TILE_WIDTH = 200
TILE_HEIGHT = 200
#floor_image = spritesheet.get_dungeon_tile(48, 32)
floor_image = spritesheet.get_tile(0, 160)
# This class will be interacted with by a Blueprint object. It basically decodes the information from the
# blueprint and then draws it. I chose this because it is a very expandable design.
# should store a set of enemies
# Figure out how to add the room type to this object, it's what is being returned. Can probably do this in the
# draw_level method
class Room:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[None for x in range(width)] for y in range(height)]
        self.room_type = None
        self.cleared = False
        # I'm going to worry about the special features later

    def set_tile(self, x, y, tile):
        self.tiles[y][x] = tile

    def add_feature(self, x, y, feature):
        pass

    # Take the floors on each far side of the room, which would be the openings, and create walls there to shut the player
    # into the room.
    def shut_room(self):
        overlay_room = Room(self.width, self.height)
        for row_num, row in enumerate(self.tiles):
            for tile_number, tile in enumerate(row):
                if row_num == 0 and tile == "floor":
                    overlay_room.set_tile(tile_number, row_num, "wall")
                elif row_num == self.height - 1 and tile == "floor":
                    overlay_room.set_tile(tile_number, row_num, "wall")
                elif tile_number == 0 and tile == "floor":
                    overlay_room.set_tile(tile_number, row_num, "wall")
                elif tile_number == self.width - 1 and tile == "floor":
                    overlay_room.set_tile(tile_number, row_num, "wall")
        
        walls, floors = overlay_room.create_room(self.top_left[0], self.top_left[1])
        del(overlay_room)
        return walls

    # This method will find an xy coordinate in the room that the enemy will spawn at.
    # This position has to be an alright distance from the player. We don't want them to spawn on the player.
    # We'll say 200 pixels from the player?
    def select_random_position(self, WIDTH, HEIGHT):
        '''rand_angle = random.randrange(0, 3)
        x = WIDTH / 2 - math.cos(rand_angle) * 200
        y = HEIGHT / 2 - math.sin(rand_angle) * 200'''
        x = random.randrange(int(self.top_left[0] + 250), int(self.bot_right[0] - 250))
        y = random.randrange(int(self.top_left[1] + 250), int(self.bot_right[1] - 250))
        return x, y

    # This will be called after the room shuts to create the enemy setup and spawn them.
    '''Current Room Types and their DC
    Normal: 12
    Hub: 16
    Enemies and their costs
    Small: 4
    Normal: 2
    Big: 3
    '''
    def start_fight(self, WIDTH, HEIGHT, player_one, PLAYER_WIDTH, PLAYER_HEIGHT):
        # default DC is for a normal room
        DC = 12
        enemies = []
        if self.room_type == "hub":
            DC = 16
        
        while DC > 2:
            new_enemy_type = random.choice(["small", "normal", "big"])
            if new_enemy_type == "small" and DC < 4:
                new_enemy_type == "big"
            elif new_enemy_type == "small":
                DC -= 4
            elif new_enemy_type == "normal":
                DC -= 2
            elif new_enemy_type == "big":
                DC -= 3
            enemies.append(new_enemy_type)

        # loop through list enemy types and change each element to an Enemy object
        for i in range(len(enemies)):
            posx, posy = self.select_random_position(WIDTH, HEIGHT)
            new_enemy = Enemy(WIDTH, HEIGHT, player_one, PLAYER_WIDTH, PLAYER_HEIGHT, enemies[i], 3.5, 1, posx, posy)
            enemies[i] = new_enemy
        
        return enemies

    def random_floor_image(self):
        image = floor_image
        if random.randint(1, 8) == 8:
            xy = random.choice([(64, 176), (112, 160), (112, 176), (32, 176)])
            image = spritesheet.get_tile(xy[0], xy[1])

        return image

    # This will be the method in charge of drawing the room! I'm going to start simple at first, but this
    # method will grow into a very large one as we add features to the game. It will return a list of sprites
    # So they can be added to sprite groups in the main script
    def create_room(self, x, y):
        # Stores the top left and bottom right coordinate for later use.
        self.top_left = [x, y]
        self.bot_right = [x + TILE_WIDTH * self.width, y + TILE_HEIGHT * self.height]

        walls = []
        floors = []
        # loop through the 2d list, and create the sprites for the tiles as we go.
        for y_level, row in enumerate(self.tiles):
            temp_x = x
            for tile_number, tile in enumerate(row):
                # Initialize these as false values so if they don't get set we don't error out
                floor = False
                under_floor = False
                wall = False
                
                # TODO TODO TODO Change each wall to grab a wall asset from the spreadsheet. We're changing them all to 
                # Squares so that the walls on the left and right aren't weird sizes anymore.
                if tile == "wall":
                    WALL_WIDTH, WALL_HEIGHT = TILE_WIDTH, TILE_HEIGHT
                    # under_floor = Floor(floor_image, TILE_WIDTH, TILE_HEIGHT, temp_x, y)
                    image = spritesheet.get_tile(16, 112) # TODO middle of room wall, change to something different
                    # Top row wall
                    if y_level == 0:
                        image = spritesheet.get_dungeon_tile(32, 16) # FIX THIS\/                    # Bottom row wall
                    elif y_level == len(self.tiles) - 1:
                        under_floor = None
                        image = spritesheet.get_dungeon_tile(48, 64) # FIX THIS
                    # Left side wall
                    elif tile_number == 0:
                        under_floor = None
                        image = spritesheet.get_dungeon_tile(16, 32) # FIX THIS
                    # Right side wall
                    elif tile_number == len(row) - 1:
                        under_floor = None
                        image = spritesheet.get_dungeon_tile(80, 32) # FIX THIS
                        
                    else:
                        # This is for the case that the wall is on the inside of the room.
                        WALL_WIDTH, WALL_HEIGHT = TILE_WIDTH, TILE_HEIGHT
                        # The under floor is here in case we want to change the size of interior walls later
                        # under_floor = Floor(floor_image, TILE_WIDTH, TILE_HEIGHT, temp_x, y)
                    # Something going on with the hallways.
                    if self.room_type != "hallway":
                        if y_level == 0 and tile_number == 0:
                            image = spritesheet.get_dungeon_tile(16, 16)
                            under_floor == None
                        if y_level == 0 and tile_number == len(row) - 1:
                            image = spritesheet.get_dungeon_tile(80, 16)
                            under_floor == None
                        if y_level == len(self.tiles) - 1 and tile_number == 0:
                            image = spritesheet.get_dungeon_tile(16, 64)
                            under_floor == None
                        if y_level == len(self.tiles) - 1 and tile_number == len(row) - 1:
                            image = spritesheet.get_dungeon_tile(80, 64)
                            under_floor == None
                    
                    wall = Wall(image, WALL_WIDTH, WALL_HEIGHT, temp_x, y)

                    temp_x += WALL_WIDTH

                if tile == "floor" or tile == "door":
                    image = self.random_floor_image()
                    if y_level == len(self.tiles) - 1:
                        floor = Floor(image, TILE_WIDTH, TILE_HEIGHT/2, temp_x, y)
                    else:
                        floor = Floor(image, TILE_WIDTH, TILE_HEIGHT, temp_x, y)
                    temp_x += TILE_WIDTH

                if under_floor:
                    floors.append(under_floor)
                if floor:
                    floors.append(floor)
                if wall:
                    walls.append(wall)
                
                if not tile:
                    temp_x += TILE_WIDTH

                # TODO Walls need to be appended second so they are rendered on top of floors!!
            y += TILE_HEIGHT
        return walls, floors



class Blueprint:
    # The class will take in a dictionary containing a 2d list, special features, and maybe other stuff down the road
    def __init__(self, setup):
        self.layout = setup['layout']
        if setup['special_features']:
            self.special_features = setup['special_features']
        else:
            self.special_features = {}
    
    def apply(self, room):
        '''This is a little complicated. We're looping through our the 2d list of tiles, then we are going to 
        apply these tile types to coordinates in a Room object. Then, the room object will have methods to 
        generate these things on the screen'''
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                room.set_tile(x, y, tile)
        for feature, positions in self.special_features.items():
            for x, y in positions:
                room.add_feature(x, y, feature)

def draw_flow(flow, start_x, start_y):
    pass