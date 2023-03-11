# Contains the board array class
from enum import Enum
import pieces
import config
from config import Player as p 
from config import Orientation as ori

class Board():
    # The board class - contains pieces and possible actions  
    
    class Field():
        # Contains Reserved state, Peice or None 
        def __init__(self, contents=None, reserved=p.NONE) -> None:
            self.contents = contents # contains a Piece or nothing 
            self.reserved = reserved # Contains elements from the Enum Reserved 

        def __str__(self):
            if(self.contents == None):
                match self.reserved:
                    case p.NONE:
                        return " "
                    case p.BLUE:
                        return config.blue_piece("☉")
                    case p.RED:
                        return config.red_piece("☉")
                    case _:
                        return "ERROR: UNKNOWN RESERVED PLAYER"
            else:
                return self.contents.__str__()
    
    def __init__(self) -> None:
        # Define the dictionary 
        self.board = {} 
        for y in range(config.HEIGHT): 
            for x in range(config.WIDTH):
                self.board[(x, y)] = Board.Field() 
        # Make initial board
        # Generate reserved fields
        self.board[(9,0)].reserved = p.BLUE
        for y in range(1,7):
            self.board[(0,y)].reserved = p.RED
            self.board[(9,y)].reserved = p.BLUE
        self.board[(0,7)].reserved = p.RED
        self.board[(1,0)].reserved = p.BLUE
        self.board[(1,7)].reserved = p.BLUE
        self.board[(8,0)].reserved = p.RED
        self.board[(8,7)].reserved = p.RED
        # Generate Lasers
        self.board[(0,0)].contents = pieces.Laser(ori.DOWN, (0,0), p.RED)
        self.board[(9,7)].contents = pieces.Laser(ori.UP, (0,0), p.BLUE)
         
        
        self.turn = p.BLUE
        self.won = p.NONE 
    


# def rotate(self, position, rotate):
#     # takes in an orientation and a direction to turn (left = counter clockwise, right = clockwise)
#     piece: Piece = self.board[position]
#     if piece is None: raise KeyError(f'There is no piece at posistion {position}')
    
#     else:
#         raise KeyError(f'{rotate} is an illegal move') a pi
        
