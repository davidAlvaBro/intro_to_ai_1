# Contains the board array class
from enum import Enum
from pieces import Piece
import config
 

class Board():
    # The board class - contains pieces and possible actions  
    
    class Field():
        # Contains Reserved state, Peice or None 
        def __init__(self, contents=None, reserved=config.Player.NONE) -> None:
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
        
        self.turn = config.Player.BLUE
        self.won = config.Player.NONE 
    


# def rotate(self, position, rotate):
#     # takes in an orientation and a direction to turn (left = counter clockwise, right = clockwise)
#     piece: Piece = self.board[position]
#     if piece is None: raise KeyError(f'There is no piece at posistion {position}')
    
#     else:
#         raise KeyError(f'{rotate} is an illegal move') a pi
        
