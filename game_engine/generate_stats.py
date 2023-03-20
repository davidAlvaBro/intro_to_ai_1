# Contains a game instance (board + visual representation)
import board as b
import gui
import config
from MCTS import run_monte_carlo
import random 
from agents import MCagent, random_agent, rotate_king_agent
import time

agent1class = MCagent
agent2class = rotate_king_agent

#"initial_random_games":1, "mc_n_iterations": 20
args1 = [2,200]
args2 = []


fname = time.time()

# Game loop 
if __name__ == "__main__":
    
    results = []

    for i in range(100): 
        # Make the board 
        board = b.Board()
        # Boolean that tells whether the game is over or not 
        over = False

        player1 = random.choice([config.Player.BLUE, config.Player.RED])

        # Create the agents
        agent1 = agent1class(player1, *args1)
        agent2 = agent2class(player1.change_player(), *args2)


        # Game loop
        while (not over): 
            # gui.print_board(board)
            if board.turn == agent1.player: a = agent1
            else: a = agent2
            position, (direction, rotate) = a.get_action(board)

            board, _, _ = b.step(board, position, rotate, direction)
            # print(f"Action taken: position {position}, move {rotate, direction}") #TODO bette rprint
            over = b.goal_test(board) 
        
        # Now the game is over and we announce the winner 
        #gui.print_board(board)
        gui.gui_announce_winner(board)
        
        if board.won == agent1.player and board.turn != agent1.player: 
            results.append(1)
        elif board.won == board.won == agent1.player: 
            results.append(0.5)
        elif board.won == agent2.player and board.turn != agent2.player:
            results.append(-1)
        else: 
            results.append(-0.5)
        print(f"Results: {results}")

        with open(f"results_{agent1}{agent2}.txt", "a") as f:
            f.write(str(results[-1]) + "\n")


print(results)
#res_pd = pd.DataFrame(results)
#res_pd.to_csv("results.csv", index=False)
        
        

        
