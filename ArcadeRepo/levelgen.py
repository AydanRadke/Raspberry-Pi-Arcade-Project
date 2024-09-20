import pygame
from pygame.locals import *
import rooms.roomconfig as rc
from classes.wall import Wall
from classes.floor import Floor

TILE_WIDTH = 200
TILE_HEIGHT = 200

# This class will be interacted with by a Blueprint object. It basically decodes the information from the
# blueprint and then draws it. I chose this because it is a very expandable design.
class Room:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[None for x in range(width)] for y in range(height)]
        # I'm going to worry about the special features later

    def set_tile(self, x, y, tile):
        self.tiles[y][x] = tile

    def add_feature(self, x, y, feature):
        pass

    # This will be the method in charge of drawing the room! I'm going to start simple at first, but this
    # method will grow into a very large one as we add features to the game. It will return a list of sprites
    # So they can be added to sprite groups in the main script
    def create_room(self, x, y):
        sprites = []
        # loop through the 2d list, and create the sprites for the tiles as we go.
        for y_level, row in enumerate(self.tiles):
            temp_x = x
            for tile_number, tile in enumerate(row):
                if tile == "wall":
                    # Top row wall
                    if y_level == 0:
                        # TODO Change constant values to something that scales with screen size later!!
                        WALL_WIDTH, WALL_HEIGHT = TILE_WIDTH, TILE_HEIGHT
                    # Bottom row wall
                    elif y_level == len(self.tiles) - 1:
                        WALL_WIDTH, WALL_HEIGHT = TILE_WIDTH, TILE_HEIGHT/2
                    # Left side wall
                    elif tile_number == 0:
                        WALL_WIDTH, WALL_HEIGHT = TILE_WIDTH/2, TILE_HEIGHT
                    # Right side wall
                    elif tile_number == len(row) - 1:
                        WALL_WIDTH, WALL_HEIGHT = TILE_WIDTH/2, TILE_HEIGHT
                        temp_x += TILE_WIDTH - WALL_WIDTH

                    image = pygame.image.load('ArcadeRepo/assets/woodenwall.jpg')
                    sprite = Wall(image, WALL_WIDTH, WALL_HEIGHT, temp_x, y)
                    if WALL_WIDTH < TILE_WIDTH:
                        temp_x += TILE_WIDTH - WALL_WIDTH
                    temp_x += WALL_WIDTH

                # TODO do the floors later ig
                if tile == "floor":
                    temp_x += TILE_WIDTH

                sprites.append(sprite)
            y += TILE_HEIGHT
            print("x should reset!!")
        return sprites



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


def draw_room(room_list, starting_point):
    pass

def level_generation():
    pass