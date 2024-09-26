'''This is our class for flows. This is the node class, it enables us to give a room a list of child rooms.
 We're going to use these to decide the relationships between rooms, and how they link together.'''

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

        
