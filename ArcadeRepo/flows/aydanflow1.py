'''This is our first flow. It's just a tree of room types.'''
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flows.node import Node

aydanflow1 = Node('spawn')
room = Node('normal')

hub = Node('hub')
hub.add_child(Node('normal').add_child(Node('normal').add_child(Node('boss'))))
hub.add_child(Node('normal').add_child(Node('treasure')))
hub.add_child(Node('normal').add_child(Node('normal').add_child(Node('shop'))))

room.add_child(hub)
room.add_child(Node('normal').add_child(Node('treasure')))

aydanflow1.add_child(room)

# print(aydanflow1)
