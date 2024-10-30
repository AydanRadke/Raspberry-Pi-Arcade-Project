'''This is our first flow. It's just a tree of room types.'''
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flows.node import Node

aydanflow1 = Node('normal')
room = Node('normal')
room.add_child(Node('normal').add_child(Node('treasure')))

hub = Node('hub')
hub.add_child(Node('normal').add_child(Node('treasure')))
hub.add_child(Node('normal').add_child(Node('normal').add_child(Node('shop'))))
hub.add_child(Node('normal').add_child(Node('normal').add_child(Node('normal'))))
room.add_child(hub)

aydanflow1.add_child(room)

# print(aydanflow1)
