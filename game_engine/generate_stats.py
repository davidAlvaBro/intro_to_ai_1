# Contains a game instance (board + visual representation)
import board as b
import gui
import config
from MCTS import run_monte_carlo
import random 
from random_agent import random_agent
#import pandas as pd


# Game loop 
if __name__ == "__main__":
    results = []
    
    for i in range(100): 
        # Make the board 
        board = b.Board()
        # Boolean that tells whether the game is over or not 
        over = False

        ai_player = random.choice([config.Player.BLUE, config.Player.RED])
        random_player = random_agent()

        print(f"The AI player is: {ai_player}")
        
        # Game loop
        while (not over): 
            # gui.print_board(board)
            if board.turn == ai_player: 
                # Run the AI 
                position, rotate, direction, root, child = run_monte_carlo(board, config.MC_N_ITERATIONS)
                # print(child)
            else:
                position, (direction, rotate) = random_player.get_random_move(board)
            
            board, _, _ = b.step(board, position, rotate, direction)
            # print(f"Action taken: position {position}, move {rotate, direction}") #TODO bette rprint
            over = b.goal_test(board) 
        
        # Now the game is over and we announce the winner 
        #gui.print_board(board)
        gui.gui_announce_winner(board)
        
        if board.won == ai_player and board.turn != ai_player: 
            results.append(1)
        elif board.won == ai_player: 
            results.append(0.5)
        elif board.won != ai_player and board.turn == ai_player: 
            results.append(-1)
        else: 
            results.append(-0.5)
        print(f"Results: {results}")
print(results)
#res_pd = pd.DataFrame(results)
#res_pd.to_csv("results.csv", index=False)
        
        

        
