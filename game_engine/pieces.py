from enum import Enum

# Contains the classes of the pieces 

'''
Overview of pieces
Searched with: https://shapecatcher.com/index.html
Orientations: Up - Right - Down - Left
Laser: ᕫᕮᕬᕭ
Deflector: ⌞⌜⌝⌟ 
Defender: ⊤⊣⊥⊢
Switch: ⟋⟍⟋⟍
King: M
Reserved: ☉
'''

class Orientation(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class LaserOptions(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    DEAD = 4 
    STOP = 5 

class Piece():
    def __init__(self, orientation, position, player):
        # Every piece needs a position and a orientation 
        self.orientation = orientation
        self.position = position
        self.player = player
        self.symbols = None
        self.piece = None
    
    def laser_interaction(self, laser_from_direction):
        raise NotImplementedError
        # TODO laser interaction - overwritten in all pieces 

class King(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "MMMM"
        self.piece = "King"

    def laser_interaction(self, laser_from_direction): # King dies when hit from all directions
        return LaserOptions.DEAD
        
class Switch(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "⟋⟍⟋⟍"
        self.piece = "Switch"

    def laser_interaction(self, laser_from_direction): # Reflects incoming lasers from a to b and from c to d (and reversed)
        self.a = (Orientation.DOWN.value + self.orientation ) % 4 
        self.b = (Orientation.LEFT.value + self.orientation ) % 4
        self.c = (Orientation.UP.value + self.orientation ) % 4
        self.d = (Orientation.RIGHT.value + self.orientation ) % 4
        if laser_from_direction == self.a:
            return (self.b + 2) % 4
        elif laser_from_direction == self.b:
            return (self.a + 2) % 4 
        elif laser_from_direction == self.c:
            return (self.d + 2) % 4
        elif laser_from_direction == self.d:
            return (self.c + 2) % 4

class Defender(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "⊤⊣⊥⊢"
        self.piece = "Defender"
    
    def laser_interaction(self, laser_from_direction): # Stops when defender is orientated opposite of laser direction 
        if laser_from_direction == (self.orientation + 2) % 4:
            return LaserOptions.STOP
        else:
            return LaserOptions.DEAD

class Deflector(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "⌞⌜⌝⌟"
        self.piece = "Deflector"
        
    def laser_interaction(self, laser_from_direction): # Reflects incoming lasers from a to b (and reversed)
        self.a = (Orientation.DOWN.value + self.orientation ) % 4
        self.b = (Orientation.LEFT.value + self.orientation ) % 4
        if laser_from_direction == self.a:
            return (self.b + 2) % 4
        elif laser_from_direction == self.b :
            return (self.a + 2) % 4 
        else:
            return LaserOptions.DEAD

class Laser(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "ᕫᕮᕬᕭ"
        self.piece = "Laser"
    
    def laser_interaction(self, laser_from_direction): # Laser stops when hit from all directions
        return LaserOptions.STOP
    
if __name__ == "__main__":
    pass