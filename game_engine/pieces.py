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

class Switch(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "⟋⟍⟋⟍"
        self.piece = "Switch"

class Defender(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "⊤⊣⊥⊢"
        self.piece = "Defender"

class Deflector(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "⌞⌜⌝⌟"
        self.piece = "Deflector"

class Laser(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "ᕫᕮᕬᕭ"
        self.piece = "Laser"
    
if __name__ == "__main__":
    pass