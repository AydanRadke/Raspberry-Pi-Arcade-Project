'''This is our first flow. It's just a tree of room types.'''

from node import Node

aydanflow1 = Node('spawn')
room = Node('normal')
room.add_child(Node('normal').add_child(Node('treasure')))

hub = Node('hub')
hub.add_child(Node('normal').add_child(Node('treasure')))
hub.add_child(Node('normal').add_child(Node('normal').add_child(Node('shop'))))
hub.add_child(Node('normal').add_child(Node('normal').add_child(Node('normal'))))
room.add_child(hub)

aydanflow1.add_child(room)

print(aydanflow1)
