'''This is our class for flows. This is the node class, it enables us to give a room a list of child rooms.
 We're going to use these to decide the relationships between rooms, and how they link together.'''
import random
import sys
import os
# Add the ArcadeRepo directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now we can import from rooms
from rooms import roomconfig
import levelgen

def find_room_and_hallway_cords(direction, parent, room, hallway_layout, door_coordinate):
    if direction == "right":
        y_shift = (parent.height - room.height) / 2 * 200
        x_shift = 0
        room_x = parent.bot_right[0] + len(hallway_layout[0]) * 200
        room_y = parent.top_left[1]
        hallway_x = parent.bot_right[0]
        hallway_y = parent.top_left[1] + (door_coordinate[1] - 1) * 200
    if direction == "left":
        y_shift = (parent.height - room.height) / 2 * 200
        x_shift = 0
        room_x = parent.top_left[0] - (len(hallway_layout[0]) + room.width) * 200
        room_y = parent.top_left[1]
        hallway_x = parent.top_left[0] - len(hallway_layout[0]) * 200
        hallway_y = parent.top_left[1] + (door_coordinate[1] - 1) * 200
    if direction == "up":
        y_shift = 0
        x_shift = (parent.width - room.width) / 2 * 200
        room_x = parent.top_left[0]
        room_y = parent.top_left[1] - (len(hallway_layout) - 2 + room.height) * 200
        hallway_x = parent.top_left[0] + (door_coordinate[0] - 1) * 200
        hallway_y = parent.top_left[1] - (len(hallway_layout) - 1) * 200
    if direction == "down":
        y_shift = 0
        x_shift = (parent.width - room.width) / 2 * 200
        room_x = parent.top_left[0]
        room_y = parent.bot_right[1] + ((len(hallway_layout) - 2) * 200)
        hallway_x = parent.top_left[0] + (door_coordinate[0] - 1) * 200
        hallway_y = parent.bot_right[1] - 200 # need to move the hallway up a tile length
    
    return room_x + x_shift, room_y + y_shift, hallway_x, hallway_y
            


# takes in the parent room object, and then selects a door on the room, and then generates a hallway distance.
# This will at some point loop until it generates a room that does not intersect with any other hallways or rooms
# maybe this function can take care of drawing the hallway too? TODO
# TODO Make this compare to all other rooms so that we don't have overlaps
def select_door_and_distance(parent, rooms, intended_room):
    door_indexes = []
    for y, list in enumerate(parent.tiles):
        for x, tile in enumerate(list):
            if tile == "door":
                door_indexes.append((x, y))
    door_coordinate = random.choice(door_indexes)

    # Generates the layout of a hallway depending on a random tile distance
    hallway_distance = random.randrange(4, 6)
    # right wall door
    if door_coordinate[0] == parent.width - 1:
        hallway_blueprint = [
            ["wall" for x in range(hallway_distance)],
            ["floor" for x in range(hallway_distance)],
            ["wall" for x in range(hallway_distance)]
                            ]
        direction = "right"
    # left wall door
    elif door_coordinate[0] == 0:
        hallway_blueprint = [
            ["wall" for x in range(hallway_distance)],
            ["floor" for x in range(hallway_distance)],
            ["wall" for x in range(hallway_distance)]
                            ]
        direction = "left"
    # top wall door
    elif door_coordinate[1] == 0:
        hallway_blueprint = [["wall", "floor", "wall"] for x in range(hallway_distance)] + [[None, None, None]]
        direction = "up"
    # bottom wall door
    elif door_coordinate[1] == parent.height - 1:
        hallway_blueprint = [["wall", "floor", "wall"] for x in range(hallway_distance)]
        direction = "down"

    return door_coordinate, hallway_blueprint, direction


def select_file_from_folder(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return random.choice(files)

def choose_room(room_type):
    if room_type == "hub":
        file = select_file_from_folder('C:\STEM\Raspberry-Pi-Arcade-Project\ArcadeRepo\\rooms\hub')
        file = file[:-3]
        room = roomconfig.config[room_type][file]
    elif room_type == 'normal':
        file = select_file_from_folder('C:\STEM\Raspberry-Pi-Arcade-Project\ArcadeRepo\\rooms\\normal')
        file = file[:-3]
        room = roomconfig.config[room_type][file]
    elif room_type == 'spawn':
        file = select_file_from_folder('C:\STEM\Raspberry-Pi-Arcade-Project\ArcadeRepo\\rooms\spawn')
        file = file[:-3]
        room = roomconfig.config[room_type][file]
    elif room_type == 'shop':
        room = roomconfig.config[room_type]
    elif room_type == 'treasure':
        room = roomconfig.config[room_type]
    
    return room


class Node:
    def __init__(self, room_type):
        self.room_type = room_type
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        return self

    def __repr__(self, level=0):
        indent = '  ' * level
        # Start with the current node's room_type
        statement = f"{indent}{self.room_type}\n"
        for child in self.children:
            statement += child.__repr__(level + 1)  # Increase level for child indentation
        return statement

    def draw_level(self, start_x=None, start_y=None, parent=None, other_rooms=None):
        rooms = []
        walls = []
        floors = []
        # Choose the room, create blueprint, apply it, then draw the room
        room = choose_room(self.room_type)
        blueprint = levelgen.Blueprint(room)
        room = levelgen.Room(len(blueprint.layout[0]), len(blueprint.layout))
        blueprint.apply(room)
        # if a parent room exists
        if parent:
            door_coordinate, hallway_layout, direction = select_door_and_distance(parent, other_rooms, room)
            parent.tiles[door_coordinate[1]][door_coordinate[0]] = "floor"
            
            # Change the new room's door to a floor so we don't generate a child room there
            if direction == "right":
                door_x = len(room.tiles[0]) - 1
                door_y = False
            if direction == "left":
                door_x = 0
                door_y = False
            if direction == "up":
                door_x = False
                door_y = 0
            if direction == "down":
                door_x = False
                door_y = len(room.tiles)
            
            if door_x or door_x == 0:
                for row in range(len(room.tiles)):
                    if room.tiles[row][door_x] == "door":
                        door_y = row
            else:
                door_x = room.tiles[door_y].index("door")
            
            room.tiles[door_y][door_x] = "floor"
            # create room based on parent's coordinates. All the subraction in the len(layout) * 200
            # statements ensure that the hallways touch the room how we want them to. They can be adjusted later.
            
            room_x, room_y, hallway_x, hallway_y = find_room_and_hallway_cords(direction, parent, room, hallway_layout, door_coordinate)
            # Need to add hallway now
            hallway = levelgen.Room(len(hallway_layout[0]), len(hallway_layout))
            for y, row in enumerate(hallway_layout):
                for x, tile in enumerate(row):
                    hallway.set_tile(x, y, tile)
            
            hallway_walls, hallway_floors = hallway.create_room(hallway_x, hallway_y)  
            # add next room
            new_walls, new_floors = room.create_room(room_x, room_y)          
            
            for wall in hallway_walls:
                walls.append(wall)
            for floor in hallway_floors:
                floors.append(floor)
            
        else:
            new_walls, new_floors = room.create_room(start_x, start_y)
        

        # Add new sprites
        for wall in new_walls:
            walls.append(wall)
        for floor in new_floors:
            floors.append(floor)
        
        # TODO Fence post is done, now we need to handle children
        if self.children:
            for num, child in enumerate(self.children):
                new_rooms, new_walls, new_floors, new_self = child.draw_level(parent=room) # need to add args for this
                # make sure that the doors get changed, so we don't accidentally select the same one twice
                room.tiles = new_self.tiles
                
                # Add new sprites and rooms
                for wall in new_walls:
                    walls.append(wall)
                for floor in new_floors:
                    floors.append(floor)
                for room in new_rooms:
                    rooms.append(room)

            # block doors by creating an empty layout, looping through the parent room to find unused doors
            # and adding it on top of the existing room
            '''block_doors = [[None for x in range(room.width)] for x in range(room.height)]
            overlay_room = levelgen.Room(len(block_doors), len(block_doors[0]))
            for y, row in enumerate(room.tiles):
                for x, tile in enumerate(row):
                    if tile == "door":
                        block_doors[y][x] = "wall"
                    overlay_room.set_tile(x, y, block_doors[y][x])
            
            overlay_walls, overlay_floors = overlay_room.create_room(start_x, start_y)
            for wall in overlay_walls:
                walls.append(wall)'''

            

        rooms.append(room)
        
        return rooms, walls, floors, parent
            


