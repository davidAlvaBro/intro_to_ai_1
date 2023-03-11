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
        # Generate Deflectors
        self.board[(0,3)].contents = pieces.Deflector(ori.UP, (0,3), p.RED)
        self.board[(0,4)].contents = pieces.Deflector(ori.RIGHT, (0,4), p.RED)
        self.board[(2,1)].contents = pieces.Deflector(ori.DOWN, (2,1), p.RED)
        self.board[(6,5)].contents = pieces.Deflector(ori.RIGHT, (6,5), p.RED)
        self.board[(7,0)].contents = pieces.Deflector(ori.RIGHT, (7,0), p.RED)
        self.board[(7,3)].contents = pieces.Deflector(ori.RIGHT, (7,3), p.RED)
        self.board[(7,4)].contents = pieces.Deflector(ori.UP, (7,4), p.RED)
        self.board[(2,3)].contents = pieces.Deflector(ori.DOWN, (2,3), p.BLUE)
        self.board[(2,4)].contents = pieces.Deflector(ori.LEFT, (2,4), p.BLUE)
        self.board[(2,7)].contents = pieces.Deflector(ori.LEFT, (2,7), p.BLUE)
        self.board[(3,2)].contents = pieces.Deflector(ori.LEFT, (3,2), p.BLUE)
        self.board[(7,6)].contents = pieces.Deflector(ori.UP, (7,6), p.BLUE)
        self.board[(9,3)].contents = pieces.Deflector(ori.LEFT, (9,3), p.BLUE)
        self.board[(9,4)].contents = pieces.Deflector(ori.DOWN, (9,4), p.BLUE)
        # Generate Switches
        self.board[(4,3)].contents = pieces.Switch(ori.RIGHT, (4,3), p.RED)
        self.board[(5,3)].contents = pieces.Switch(ori.UP, (5,3), p.RED)
        self.board[(4,4)].contents = pieces.Switch(ori.UP, (4,4), p.BLUE)
        self.board[(5,4)].contents = pieces.Switch(ori.RIGHT, (5,4), p.BLUE)
        # Generate Defenders
        self.board[(4,0)].contents = pieces.Defender(ori.DOWN, (4,0), p.RED)
        self.board[(6,0)].contents = pieces.Defender(ori.DOWN, (6,0), p.RED)
        self.board[(3,7)].contents = pieces.Defender(ori.UP, (3,7), p.BLUE)
        self.board[(5,7)].contents = pieces.Defender(ori.UP, (5,7), p.BLUE)
        # Generate Kings
        self.board[(5,0)].contents = pieces.King(ori.DOWN, (5,0), p.RED)
        self.board[(4,7)].contents = pieces.King(ori.UP, (4,7), p.BLUE)
        
        
        self.turn = p.BLUE
        self.won = p.NONE 
    


# def rotate(self, position, rotate):
#     # takes in an orientation and a direction to turn (left = counter clockwise, right = clockwise)
#     piece: Piece = self.board[position]
#     if piece is None: raise KeyError(f'There is no piece at posistion {position}')
    
#     else:
#         raise KeyError(f'{rotate} is an illegal move') a pi
        
