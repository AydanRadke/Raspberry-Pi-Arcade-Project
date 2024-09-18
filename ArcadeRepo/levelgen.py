import pygame
from pygame.locals import *
import rooms.roomconfig as rc

# This class will be interacted with by a Blueprint object. It basically decodes the information from the
# blueprint and then draws it. I chose this because it is a very expandable design.
class Room:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # TODO set up tiles and feature variables, and then finish the other methods

    def set_tile(self, x, y, tile):
        pass

    def add_feature(self, x, y, feature):
        pass

    def create_room(self):
        pass

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