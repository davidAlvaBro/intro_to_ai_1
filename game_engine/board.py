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
    
    def sum_coordinates(coord1, coord2) -> tuple:
        # add's coord2 to coord1 
        return tuple([sum(x) for x in zip(coord1, coord2)])
    
    def __init__(self) -> None:
        # Define the dictionary 
        self.board = {} 
        for row in range(config.HEIGHT): 
            for column in range(config.WIDTH):
                self.board[(row, column)] = Board.Field() 
        # Make initial position
            # Generate pieces and fields 
        
        self.turn = Player.BLUE
    
    # TODO the below should be in game.py not here 
    def is_legal_action(self, position, rotate='No', direction='No') -> bool:
        illigal_move = False 
        if self.board[position].contents != None: 
            # TODO Check if both direction and rotate is set? or do we check that earlier? 
            if direction != 'No': 
                # TODO Check if it is the players piece 
                
                # TODO Check if it is the laser !!!
                
                # Check if the destination is empty and if it is legal to move to the field 
                destination = self.board[Board.sum_coordinates(position, direction)] 
                if destination.contents != None: 
                    illigal_move = True 
                elif destination.reserved != self.turn: 
                    illigal_move = True 
            elif rotate != 'No':
                pass # This cannot make any errors      
        else: 
            illigal_move = True 
        
        return illigal_move
    
    def action(self, position, rotate='No', direction='No'):
        # Check if it is a legal move 
        is_legal = self.is_legal_action(position, rotate='No', direction='No')
       
        if is_legal:  # Make the legal move 
            if rotate != 'No': 
                if rotate == Rotate.RIGHT: # turning right adds 1 to the position (see table Move)
                    self.board[position].contents.orientation = (self.board[position].contents.orientation + 1) % 4
                elif rotate == Rotate.LEFT:
                    self.board[position].contents.orientation = (self.board[position].contents.orientation - 1) % 4
            elif direction != 'No':
                self.board[Board.sum_coordinates(position, direction)].contents = self.board[position].contents
                self.board[position] = None
        else:
            pass # TODO return to the UI that it does not work 
    
    # TODO step := action -> laser (kill piece?) -> change turn -> goal_test 
    # TODO use visual representation/GUI 
    


# def rotate(self, position, rotate):
#     # takes in an orientation and a direction to turn (left = counter clockwise, right = clockwise)
#     piece: Piece = self.board[position]
#     if piece is None: raise KeyError(f'There is no piece at posistion {position}')
    
#     else:
#         raise KeyError(f'{rotate} is an illigal move') a pi
        
