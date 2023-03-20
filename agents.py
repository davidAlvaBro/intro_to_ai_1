import config 
import board as b
import random
from ai.MCTS import run_monte_carlo


class MCagent:
    def __init__(self, player, initial_random_games = config.INITIAL_RANDOM_GAMES,
                       mc_n_iterations = config.MC_N_ITERATIONS,
                       guided=True):
        self.initial_random_games = initial_random_games
        self.mc_n_iterations = mc_n_iterations
        self.player = player
        self.guided = guided
    
    def __repr__(self):
        return f"MCagent({self.initial_random_games}, {self.mc_n_iterations}, {self.guided})"

    def get_action(self, board: b.Board):
        """
        Get the best action from the current board using Monte Carlo Tree Search
        """
        assert board.turn == self.player, "Wrong player"

        # Get the best move from the Monte Carlo Tree Search using UCB1
        position, rotate, direction, root, child = run_monte_carlo(board, self.initial_random_games,
                                                                   self.mc_n_iterations, self.guided, self.player)
        return position, (direction, rotate)


class rotate_king_agent:

    def __init__(self, player):
        self.player = player
    
    def __repr__(self):
        return f"rotate_king_agent"

    def get_action(self, board: b.Board):
        """
        Rotate the king (which essentially does nothing)
        """
        
        assert board.turn == self.player, "Wrong player"

        if self.player == config.Player.RED:
            piece_list = board.red_pieces
        else: 
            piece_list = board.blue_pieces
        
        for piece in piece_list: 
            if piece.piece == "King": 
                piece_to_move = piece
        
        return piece_to_move.position, (None, config.Rotate.LEFT)



class random_agent: 
    def __init__(self, player):
        self.player = player
    
    def __repr__(self):
        return f"random_agent"

    def get_action(self, board: b.Board):
        """
        Get a random legal move in the current board state 
        """
        assert board.turn == self.player, "Wrong player"

        if self.player == config.Player.RED:
            piece_list = board.red_pieces
        else: 
            piece_list = board.blue_pieces
        
        # Get the alive pieces and make a random choice
        alive_pieces = [piece for piece in piece_list if piece.alive]
        piece_to_move = random.choice(alive_pieces)
        
        
        # Get all possible moves 
        # possible_moves = set(r for r in config.Rotate).union(set(m for m in config.Move))
        possible_moves = [r for r in config.Rotate] + [m for m in config.Move]
        n_possible = len(possible_moves)
        
        sampled_move = None
        
        while(sampled_move == None): 
            idx = random.randint(0, n_possible-1)
            possible_move = possible_moves[idx]
            
            # See if the move is legal 
            if possible_move in config.Rotate:
                if b.is_legal_action(board, position=piece_to_move.position, direction=None, rotate=possible_move):
                    sampled_move = (None, possible_move)
                    break
            else:
                if b.is_legal_action(board, position=piece_to_move.position, direction=possible_move, rotate=None):
                    sampled_move = (possible_move, None)
                    break
            
            # Else remove that from the set
            possible_moves[idx] = possible_moves[n_possible-1]
            n_possible -= 1
            assert n_possible > 0, "No legal moves"
            
        # Return a piece and an action (tuple (direction, rotate)) 
        return piece_to_move.position, sampled_move
