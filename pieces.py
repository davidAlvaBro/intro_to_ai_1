import config

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
# TODO Change the .values to make laser orientation an orientation instead of a value 

class Piece():
    def __init__(self, orientation, position, player):
        # Every piece needs a position and a orientation 
        self.orientation = orientation
        self.position = position
        self.player = player
        self.symbols = None
        self.piece = None
        self.alive = True
    
    def kill(self):
        self.orientation = None
        self.position = None
        self.alive = False

    def rotate(self, rotate):
        if rotate == config.Rotate['LEFT']:
            self.orientation = (self.orientation - 1) % 4
        if rotate == config.Rotate['RIGHT']:
            self.orientation = (self.orientation + 1) % 4
    
    def take_snapshot(self):
        return {"orientation": self.orientation,
                "position": self.position,
                "alive": self.alive}

    def restore_from_snapshot(self, snapshot):
        self.orientation = snapshot["orientation"]
        self.position = snapshot["position"]
        self.alive = snapshot["alive"]

    def __str__(self):
        if self.player == config.Player.RED:
            return config.red_piece(self.symbols[self.orientation.value])
        elif self.player == config.Player.BLUE:
            return config.blue_piece(self.symbols[self.orientation.value])
        else:
            return "ERROR: Unknown Player"

    def laser_interaction(self, laser_from_direction):
        raise NotImplementedError
        # Overwritten in all pieces 
    
class King(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "MMMM"
        self.piece = "King"

    def laser_interaction(self, laser_from_direction): # King dies when hit from all directions
        return config.LaserOptions.DEAD
    
        
class Switch(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "⟋⟍⟋⟍"
        self.piece = "Switch"

    def laser_interaction(self, laser_from_direction): # Reflects incoming lasers from a to b and from c to d (and reversed)
        self.a = (config.Orientation.DOWN.value + self.orientation.value ) % 4 
        self.b = (config.Orientation.RIGHT.value + self.orientation.value ) % 4
        self.c = (config.Orientation.UP.value + self.orientation.value ) % 4
        self.d = (config.Orientation.LEFT.value + self.orientation.value ) % 4
        if laser_from_direction.value == self.a:
            return config.LaserOptions((self.b + 2) % 4)
        elif laser_from_direction.value == self.b:
            return config.LaserOptions((self.a + 2) % 4)
        elif laser_from_direction.value == self.c:
            return config.LaserOptions((self.d + 2) % 4)
        elif laser_from_direction.value == self.d:
            return config.LaserOptions((self.c + 2) % 4)
    

class Defender(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "⊤⊣⊥⊢"
        self.piece = "Defender"
    
    def laser_interaction(self, laser_from_direction): # Stops when defender is orientated opposite of laser direction 
        if laser_from_direction.value == (self.orientation.value + 2) % 4:
            return config.LaserOptions.STOP
        else:
            return config.LaserOptions.DEAD

class Deflector(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "⌞⌜⌝⌟"
        self.piece = "Deflector"
        
    def laser_interaction(self, laser_from_direction): # Reflects incoming lasers from a to b (and reversed)
        self.a = (config.Orientation.DOWN.value + self.orientation.value ) % 4
        self.b = (config.Orientation.LEFT.value + self.orientation.value ) % 4
        if laser_from_direction.value == self.a:
            return config.LaserOptions((self.b + 2) % 4)
        elif laser_from_direction.value == self.b :
            return config.LaserOptions((self.a + 2) % 4)
        else:
            return config.LaserOptions.DEAD

class Laser(Piece):
    def __init__(self, orientation, position, player):
        super().__init__(orientation=orientation, position=position, player=player)
        self.symbols = "ᕫᕮᕬᕭ"
        self.piece = "Laser"
    
    def laser_interaction(self, laser_from_direction): # Laser stops when hit from all directions
        return config.LaserOptions.STOP
    
if __name__ == "__main__":
    pass