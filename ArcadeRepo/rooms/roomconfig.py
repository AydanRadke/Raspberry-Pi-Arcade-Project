# This will be a dictionary that imports all of our rooms, so we can just import a dictionary when we need
# to access the rooms, but also have the modularity of giving each room its own file
import rooms.room1
import rooms.room2

config = {
    "room1": rooms.room1.room1_setup,
    "room2": rooms.room2.room2_setup
}