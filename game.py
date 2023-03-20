# Contains a game instance (board + visual representation)
import board as b
import gui
import config
from ai.MCTS import run_monte_carlo


# Game loop 
if __name__ == "__main__":
    # Make the board 
    board = b.Board()
    # Boolean that tells whether the game is over or not 
    over = False

    ai_player = config.AI_PLAYER

    # Game loop
    while (not over): 
        gui.print_board(board)
        if board.turn == ai_player: 
            # Run the AI 
            position, rotate, direction, root, child = run_monte_carlo(board, config.MC_N_ITERATIONS)
            print(child)
        else:
            position, rotate, direction = gui.gui_action_prompt(board)

        # Check if the action is legal 
        is_legal = b.is_legal_action(board, position, rotate, direction)
        
        if is_legal: 
            # Run the step function, execute action, use laser, change turn and check if done  
            board = b.step(board, position, rotate, direction)
            print(f"Action taken: position {position}, move {rotate, direction}") #TODO bette rprint
            
            over = b.goal_test(board) 
        else: 
            gui.gui_illegal_action()
    
    # Now the game is over and we announce the winner 
    gui.print_board(board)
    gui.gui_announce_winner(board)
    

    