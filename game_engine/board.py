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
        def __init__(self, contents=None, reserved=p.NONE):
            self.contents = contents # contains a Piece or nothing 
            self.reserved = reserved # Contains elements from the Enum Reserved 

        def __str__(self):
            if(self.contents == None):
                if self.reserved == p.NONE: 
                    return " " 
                elif self.reserved == p.RED:
                    return config.red_piece("☉")
                elif self.reserved == p.BLUE:
                    return config.blue_piece("☉")
                else:
                    return "ERROR: UNKNOWN RESERVED PLAYER"
                # match self.reserved:
                #     case p.NONE:
                #         return " "
                #     case p.BLUE:
                #         return config.blue_piece("☉")
                #     case p.RED:
                #         return config.red_piece("☉")
                #     case _:
                #         return "ERROR: UNKNOWN RESERVED PLAYER"
            else:
                return self.contents.__str__()
    
    def __init__(self):
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
        self.board[config.LASER_POSITION[p.RED]].contents = pieces.Laser(ori.DOWN, config.LASER_POSITION[p.RED], p.RED)
        self.board[config.LASER_POSITION[p.BLUE]].contents = pieces.Laser(ori.UP, config.LASER_POSITION[p.RED], p.BLUE)
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

        # maintain a list of pieces for each player
        # this is used when restoring the board to a previous state

        self.red_pieces = []
        self.blue_pieces = []

        for x,y in self.board:
            if self.board[(x,y)].contents != None:
                if self.board[(x,y)].contents.player == p.RED:
                    self.red_pieces.append(self.board[(x,y)].contents)
                elif self.board[(x,y)].contents.player == p.BLUE:
                    self.blue_pieces.append(self.board[(x,y)].contents)
    
    def kill_piece(self, piece: pieces.Piece):
        """
        kill a piece and remove it from the board
           - but don't remove it from the list of pieces
             as they are needed for restoring the board to 
             earlier states
        """
        self.board[piece.position].contents = None
        piece.kill()


    def take_snapshot(self):
        """
        returns a snapshot of the board
        a shapshot is a dictionary and it has the form:
        
        {
            "red": [piece_snapshot, piece_snapshot, ...],
            "blue": [piece_snapshot, piece_snapshot, ...]
        }
        
        where piece_snapshot is the snapshot of a piece
        for doc on piece snapshots, see pieces.py

        """

        snapshot = {"red": [], "blue": []}
        for piece in self.red_pieces:
            snapshot["red"].append(piece.take_snapshot())
        for piece in self.blue_pieces:
            snapshot["blue"].append(piece.take_snapshot())
    
        return snapshot
    
    def restore_from_snapshot(self, snapshot):
        """
        restores the board from a snapshot
        see take_snapshot for doc on snapshots

        """

        def update_piece_and_board(piece: pieces.Piece, piece_snapshot):
            """
            helper function for restoring each piece from a snapshot
            """
            # get current position of piece
            current_pos = piece.position
            # if current position contains the current
            # piece, remove it from that position
            if self.board[current_pos].contents == piece:
                self.board[current_pos].contents = None
            # restore piece from snapshot and move
            # it to its original (snapshot) position
            # if the piece is alive
            piece.restore_from_snapshot(piece_snapshot)
            if piece.alive:
                self.board[piece.position].contents = piece

        # restore each piece from its snapshot
        for i,piece_snapshot in enumerate(snapshot["red"]):
            piece = self.red_pieces[i]
            update_piece_and_board(piece, piece_snapshot)
        
        for i,piece_snapshot in enumerate(snapshot["blue"]):
            piece = self.blue_pieces[i]
            update_piece_and_board(piece, piece_snapshot)
    
    # def get_legal_actions(self, position: tuple):
    #     """
    #     returns a list of legal actions for the current position
    #     """
    #     # TODO: implement this method
    #     raise NotImplementedError
    #     legal_actions = []
    #     piece = self.board[position].contents
    #     if piece is None:
    #         return []
    #     if piece.player != self.turn:
    #         return []
    #     if piece.alive:
    #         if isinstance(piece, pieces.Laser):
    #             legal_actions.append("rotate")
        

# Function that adds coordinates together 
def sum_coordinates(coord1, coord2) -> tuple:
        # add's coord2 to coord1 
        return tuple([sum(x) for x in zip(coord1, coord2)])

# Function that checks if a move is legal 
def is_legal_action(board, position, rotate=None, direction=None) -> bool:
        illegal_move = False 
        if not position in board.board.keys(): 
            illegal_move = True # If the position is not on the board you can't move from there
        elif board.board[position].contents != None: # If there is no piece in the position you can't move from there
            if board.board[position].contents.player != board.turn:
                illegal_move = True # You cannot move the opponents pieces 
            elif rotate is not None:
                if direction is not None: 
                    illegal_move = True # Only way rotation can go wrong is if the player tries both rotate and move
            
            elif direction is not None: # Check if the destination is legal 
                destination = board.board[sum_coordinates(position, direction.value)] 
                if board.board[position].contents.piece == "Laser":
                    illegal_move = True # You cannot move "laser" to another location 
                elif not destination in board.board.keys(): 
                    illegal_move = True # You are moving out of the board 
                elif destination.contents is not None: 
                    illegal_move = True # You are moving onto another piece (this ain't chess)
                elif not (destination.reserved == board.turn or destination.reserved == None):
                    illegal_move = True # You can't move to your opponents reserved fields 
             
        else: 
            illegal_move = True 
        
        return illegal_move

def action(board, position, rotate=None, direction=None):
    # Take the action given and return board 
    piece = board.board[position].contents
    if rotate is not None: 
        piece.orientation.rotate(rotate) # turning right adds 1 to the position (see table Move)
    elif direction is not None:
        new_position = sum_coordinates(position, direction.value)
        piece.position = new_position
        board.board[new_position].contents = piece
        board.board[position].contents = None
    return board 
        
def fire_laser(board): 
    # returns the board after the laser has fired 
    laser_position = config.LASER_POSITION[board.turn]  
    shooter = board.board[laser_position].contents
    laser = {"orientation": shooter.orientation, "position": shooter.position}

    while (True):
        laser["position"] = sum_coordinates(laser["position"], laser["orientation"].toMove().value) 
        
        if not laser["position"] in board.board.keys(): # Check if this new position is in the board 
            break 
        
        piece = board.board[laser["position"]].contents
        if piece != None: # Check if there is a piece 
            interaction = piece.laser_interaction(laser["orientation"]) 
            
            if interaction == config.LaserOptions.STOP: # If the laser stops break 
                break 
            elif interaction == config.LaserOptions.DEAD: # If the laser kills the piece 
                if piece.piece == "King": # if it is the king then the opposite player wins  
                    board.won = piece.player.change_player()
                # board.board[laser["position"]].contents = None 
                board.kill_piece(piece)
                break 
            else: 
                laser["orientation"] = interaction # Hitting a mirror changes orientation
        
    return board 

def goal_test(board): 
    # Returns if the game is over who won and otherwise false
    if board.won == config.Player.NONE: 
        return False 
    else: 
        return True
    
def step(board, position, rotate, direction): 
    # Execute action, use laser and change turns change turn
    board = action(board, position, rotate, direction)
    
    board = fire_laser(board)
    
    board.turn = board.turn.change_player()
    
    return board

def get_legal_actions(board): 
    legal_actions = []
    player = board.turn
    if player == p.RED:
        piece_list = board.red_pieces
    else: 
        piece_list = board.blue_pieces
        
    for piece in piece_list:
        if piece.alive:
            position = piece.position
            for i in config.Rotate:
                if is_legal_action(board, position, rotate=i, direction=None):
                    legal_actions.append((piece, i))
            for i in config.Move:
                if is_legal_action(board, position, rotate=None, direction=i):
                    legal_actions.append((piece, i))
    return legal_actions
    