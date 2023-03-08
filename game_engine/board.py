# Contains the board array class
from enum import Enum
from pieces import Piece
import config

class Move(Enum):
    UP = (0,-1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT_UP = (1, -1)
    RIGHT_DOWN = (1, 1)
    LEFT_DOWN = (-1, 1)
    LEFT_UP = (-1, -1)
    
class Rotate(Enum):
    LEFT = 0
    RIGHT = 1
    
class Player(Enum):
    NONE = 0
    BLUE = 1 
    RED = 2 
 

class Board():
    # The board class - contains pieces and possible actions  
    
    class Field():
        # Contains Reserved state, Peice or None 
        def __init__(self, contents=None, reserved=Player.NONE) -> None:
            self.contents = contents # contains a Piece or nothing 
            self.reserved = reserved # Contains elements from the Enum Reserved 
    
    def __init__(self) -> None:
        # Define the dictionary 
        self.board = {} 
        for row in range(config.HEIGHT): 
            for column in range(config.WIDTH):
                self.board[(row, column)] = Board.Field() 
        # Make initial position
            # Generate pieces and fields 
        
        self.turn = Player.BLUE
        self.won = Player.NONE 
    


# def rotate(self, position, rotate):
#     # takes in an orientation and a direction to turn (left = counter clockwise, right = clockwise)
#     piece: Piece = self.board[position]
#     if piece is None: raise KeyError(f'There is no piece at posistion {position}')
    
#     else:
#         raise KeyError(f'{rotate} is an illegal move') a pi
        
