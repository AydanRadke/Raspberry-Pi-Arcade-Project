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

# I think that something is happening in this code that is making the rooms not have accurate coordinates. Should
# Check this out because we need accurate coordinates to be able to lock the player in rooms.

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
def select_door_and_distance(parent, rooms, intended_room, parent_type):
    door_indexes = []
    for y, list in enumerate(parent.tiles):
        for x, tile in enumerate(list):
            if tile == "door":
                door_indexes.append((x, y))

    # Maybe change to a for loop through door indexes?
    counter = 0
    while counter <= 15:
        counter += 1
        door_coordinate = random.choice(door_indexes)

        # Generates the layout of a hallway depending on a random tile distance
        # FOR SOME REASON, THE HALLWAYS GOING UP AND DOWN ARE SHORTER THAN THE ONES LEFT AND RIGHT
        # It doesn't hurt anything, maybe fix later idk.
        hallway_distance = 3
            

        # right wall door
        if door_coordinate[0] == parent.width - 1:
            hallway_blueprint = [
                ["wall" for x in range(hallway_distance)],
                ["floor" for x in range(hallway_distance)],
                ["wall" for x in range(hallway_distance)]
                                ]
            direction = "right"
            iroom_leftx, iroom_rightx = parent.bot_right[0], parent.bot_right[0] + (hallway_distance + intended_room.width) * 200
            iroom_topy, iroom_boty = parent.top_left[1], parent.bot_right[1]
        # left wall door TODO This isn't working right I don't think
        elif door_coordinate[0] == 0:
            hallway_blueprint = [
                ["wall" for x in range(hallway_distance)],
                ["floor" for x in range(hallway_distance)],
                ["wall" for x in range(hallway_distance)]
                                ]
            direction = "left"
            iroom_leftx, iroom_rightx = parent.top_left[0] - (hallway_distance + intended_room.width) * 200, parent.top_left[0]
            iroom_topy, iroom_boty = parent.top_left[1], parent.bot_right[1]
        # top wall door
        elif door_coordinate[1] == 0:
            hallway_blueprint = [["wall", "floor", "wall"] for x in range(hallway_distance)] + [[None, None, None]]
            direction = "up"
            iroom_leftx, iroom_rightx = parent.top_left[0], parent.bot_right[0]
            iroom_topy, iroom_boty = parent.top_left[1] - (hallway_distance + intended_room.height) * 200, parent.top_left[1]
        # bottom wall door
        elif door_coordinate[1] == parent.height - 1:
            hallway_blueprint = [["wall", "floor", "wall"] for x in range(hallway_distance)]
            direction = "down"
            iroom_leftx, iroom_rightx = parent.top_left[0], parent.bot_right[0]
            iroom_topy, iroom_boty = parent.bot_right[1], parent.bot_right[1] + (hallway_distance + intended_room.height) * 200

        generate = True
        for room in rooms:
            if not (iroom_leftx >= (room.bot_right[0]) or room.top_left[0] >= (iroom_rightx) or iroom_topy >= (room.bot_right[1]) or room.top_left[1] >= (iroom_boty)):
                # This is pretty scuffed but it's just a way to bypass a problem with
                # the rooms not wanting to go left or right of a hub
                generate = False
                if (direction == "left" or direction == "right") and parent_type == 'hub':
                    generate = True
                    print("HUB LEFT OR RIGHT ROOM CREATED")
                    print(f"Hub top left: ({parent.top_left}) Room bottom right: ({parent.bot_right})")
                    print(f"Room top left: ({iroom_leftx}, {iroom_topy}) Room bottom right: ({iroom_rightx}, {iroom_boty})")
                    return door_coordinate, hallway_blueprint, direction
                # TODO log rooms that do not get generated and the info about the rooms that stop them
                # so we can figure out why some rooms aren't being generated and why.
                # Could be because of the None lists in the hallways!!!
                # print(f"Hallway length: {hallway_distance}, Direction: {direction}")
                # print(f"Room top left: ({iroom_leftx}, {iroom_topy}) Room bottom right: ({iroom_rightx}, {iroom_boty})")
                # print(f"Blocking room top left: ({room.top_left[0]}, {room.top_left[1]}) Blocking room bottom right: ({room.bot_right[0]}, {room.bot_right[1]})")
                # print(parent_type)
                # print(parent.tiles)
            

        if generate:
            return door_coordinate, hallway_blueprint, direction
        else:
            continue
    return False, False, False


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
    elif room_type == 'boss':
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

    def draw_level(self, start_x=None, start_y=None, parent=None, other_rooms=None, parent_type=None):
        hallway = None
        rooms = []
        hallways = []
        if other_rooms:
            for r in other_rooms:
                rooms.append(r)
                
        walls = []
        floors = []
        # Choose the room, create blueprint, apply it, then draw the room
        room = choose_room(self.room_type)
        blueprint = levelgen.Blueprint(room)
        room = levelgen.Room(len(blueprint.layout[0]), len(blueprint.layout))
        blueprint.apply(room)
        # if a parent room exists
        if parent:
            # TODO SOMETHING IS GOING WRONG WITH REPLACING THE DOORS ON THE HUBS
            # HUB AND OTHER CHILDREN ARE BEING ADDED TO THE OTHER_ROOMS LIST BEFORE
            # THAT LAST ONE, could be the reason why the left one gets stopped all the time
            
            door_coordinate, hallway_layout, direction = select_door_and_distance(parent, other_rooms, room, self.room_type)
            if hallway_layout == False:
                print(f"Room failed -- {self.room_type}")
                return [], [], [], parent
            

            parent.tiles[door_coordinate[1]][door_coordinate[0]] = "floor"
            if parent_type == "hub":
                print(f"DIRECTION: {direction}")
                print(f"HUB FLOOR REPLACED: {parent.tiles}")
            # Change the new room's door to a floor so we don't generate a child room there
            if direction == "left":
                door_x = len(room.tiles[0]) - 1
                door_y = False
                print("I'm going left")
            if direction == "right":
                door_x = 0
                door_y = False
                print("I'm going right")
            if direction == "down":
                door_x = False
                door_y = 0
                print("I'm going down")
            if direction == "up":
                door_x = False
                door_y = len(room.tiles) - 1
                print("I'm going up")
            
            if door_x is not False:
                print(f"Vertical Search Entered. Direction: {direction}")
                for row in range(len(room.tiles)):
                    if room.tiles[row][door_x] == "door":
                        door_y = row
            else:
                door_x = room.tiles[door_y].index("door")
            if self.room_type == "hub":
                print(f"Hub before new floor: {room.tiles}")

            room.tiles[door_y][door_x] = "floor"
            # create room based on parent's coordinates. All the subraction in the len(layout) * 200
            # statements ensure that the hallways touch the room how we want them to. They can be adjusted later.
            if self.room_type == "hub":
                print(f"Hub Room being placed. Parent direction: {direction}")
                print(f"Hub tiles: {room.tiles}")
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
        
        room.room_type = self.room_type
        rooms.append(room)
        # We're not going to store the hallway room objects anymore. I'm sick of them.
        # Add new sprites
        for wall in new_walls:
            walls.append(wall)
        for floor in new_floors:
            floors.append(floor)
        
        # TODO Fence post is done, now we need to handle children
        if self.children:
            for num, child in enumerate(self.children):
                new_rooms, new_walls, new_floors, new_self = child.draw_level(parent=room, other_rooms=rooms, parent_type=self.room_type)
                # make sure that the doors get changed, so we don't accidentally select the same one twice
                room.tiles = new_self.tiles
                
                # Add new sprites and rooms
                for wall in new_walls:
                    walls.append(wall)
                for floor in new_floors:
                    floors.append(floor)
                for new_room in new_rooms:
                    rooms.append(new_room)

            # block doors by creating an empty layout, looping through the parent room to find unused doors
            # and adding it on top of the existing room
        block_doors = [[None for x in range(room.width)] for x in range(room.height)]
        overlay_room = levelgen.Room(len(block_doors[0]), len(block_doors))
        for y, row in enumerate(room.tiles):
            for x, tile in enumerate(row):
                if tile == "door":
                    block_doors[y][x] = "wall"
                overlay_room.set_tile(x, y, block_doors[y][x])
        
        overlay_walls, overlay_floors = overlay_room.create_room(room.top_left[0], room.top_left[1])
        for wall in overlay_walls:
            walls.append(wall)


        return rooms, walls, floors, parent
            


