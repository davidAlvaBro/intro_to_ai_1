# Contains a game instance (board + visual representation)
import board as b
import config 
import visual_representation
# TODO import GUI
# TODO fix enums in general - Rule of thumb things that can be stored as enums are stored as enums (then we can use methods for said enums)

# Function that adds coordinates together 
def sum_coordinates(coord1, coord2) -> tuple:
        # add's coord2 to coord1 
        return tuple([sum(x) for x in zip(coord1, coord2)])

# Function that checks if a move is legal 
def is_legal_action(board, position, rotate='No', direction='No') -> bool:
        illegal_move = False 
        if not position in board.board.keys(): 
            illegal_move = True # If the position is not on the board you can't move from there
        elif board.board[position].contents != None: # If there is no piece in the position you can't move from there
            if board.board[position].contents.player != board.turn:
                illegal_move = True # You cannot move the opponents pieces 
            elif rotate != 'No':
                if direction != 'No': 
                    illegal_move = True # Only way rotation can go wrong is if the player tries both 
            
            elif direction != 'No': # Check if the destination is legal 
                destination = board.board[sum_coordinates(position, direction.value)] 
                if board.board[position].piece == "Laser":
                    illegal_move = True # You cannot move "laser" to another location 
                elif not destination in board.board.keys(): 
                    illegal_move = True # You are moving out of the board 
                elif destination.contents != None: 
                    illegal_move = True # You are moving onto another piece (this ain't chess)
                elif not (destination.reserved == board.turn or destination.reserved == None):
                    illegal_move = True # You can't move to your opponents reserved fields 
             
        else: 
            illegal_move = True 
        
        return illegal_move

def action(board, position, rotate='No', direction='No'):
    # Take the action given and return board 
    if rotate != 'No': 
        if rotate == config.Rotate.RIGHT: # turning right adds 1 to the position (see table Move)
            board.board[position].contents.orientation = (board.board[position].contents.orientation + 1) % 4
        elif rotate == config.Rotate.LEFT:
            board.board[position].contents.orientation = (board.board[position].contents.orientation - 1) % 4
    elif direction != 'No':
        board.board[sum_coordinates(position, direction)].contents = board.board[position].contents
        board.board[position] = None
    return board 
        
def fire_laser(board): 
    # returns the board after the laser has fired 
    laser_position = config.laser_position[board.turn] # TODO Put this in config 
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
                board.board[laser["position"]].contents = None 
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
    
    board.turn = None # TODO HOW DO WE SWAP WITH THIS DUM NUMS! 
    
    return board

# Game loop 
if __name__ == "__main__":
    # Make the board 
    board = b.Board()
    # Boolean that tells whether the game is over or not 
    over = False
    
    while (not over): 
        # TODO Ask GUI to print board 
        visual_representation.print_board(board)
        
        # TODO Ask GUI to return action (in the format of enums)
        (position, rotate, direction) = None 

        # Check if the action is legal 
        is_legal = is_legal_action(board, position, rotate, direction)
        
        if is_legal: 
            # Run the step function, execute action, use laser, change turn and check if done  
            board = step(board, position, rotate, direction)
            
            over = goal_test(board) 
        else: 
            # TODO call GUI "not_legal_action" that informs user that the action was illegal 
            pass
    
    # Now the game is over and we announce the winner 
    # TODO call gui "announce_winner" with board.won as argument 
    

    