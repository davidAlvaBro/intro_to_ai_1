# Contains a game instance (board + visual representation)
import board as b
import gui

# Game loop 
if __name__ == "__main__":
    # Make the board 
    board = b.Board()
    # Boolean that tells whether the game is over or not 
    over = False
    
    while (not over): 
        position, rotate, direction = gui.gui_action_prompt(board)

        # Check if the action is legal 
        is_legal = b.is_legal_action(board, position, rotate, direction)
        
        if is_legal: 
            # Run the step function, execute action, use laser, change turn and check if done  
            board = b.step(board, position, rotate, direction)
            
            over = b.goal_test(board) 
        else: 
            # TODO call GUI "not_legal_action" that informs user that the action was illegal 
            pass
    
    # Now the game is over and we announce the winner 
    # TODO call gui "announce_winner" with board.won as argument 
    

    