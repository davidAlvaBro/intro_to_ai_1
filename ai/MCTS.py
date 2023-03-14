from game_engine import config
from game_engine import board
import random
import math

"""
input: board


architecture:



do:
a := get legal actions
make dead/alive lists 
for each legal action:


"""

class MCTS_node: 
    def __init__(self, board, parent) -> None:
        self.snapshot = board.take_snapshot()
        self.board = board
        self.parent = parent
        self.won_games = 0
        self.total_games = 0
        self.children = {} # key : piece_action = (pos, action) , value : node 
        self.UCB = None
        self.LCB = None
        self.play_random() 
        # Save snapshot 
        # Do play random while restore from snapshot play random X times 
    
    def update_game_counters(self, n_won, n_total):
        self.won_games += n_won
        self.total_games += n_total
        assert self.total_games >= 1, "total games cannot be less than 1"
        assert 0 <= self.won_games <= self.total_games, "won games must be in [1, total_games]"
        a = self.won_games/self.total_games
        b = math.sqrt(2*math.log(self.parent.total_games)/self.total_games)
        self.UCB = a + b
        self.LCB = a - b

    def backprop(self, n_won, n_total):
        self.update_game_counters(n_won, n_total)
        if self.parent is not None:
            self.parent.backprob(n_won, n_total)

    
    def expand(self):
        # Generate all legal actions
        # For each action generate child with correct board (restore snapshot first)
        self.board.restore_from_snapshot(self.snapshot)
        legal_actions = board.get_legal_actions(self.board)
        for action in legal_actions:
            (piece, act) = action
            if act in config.Rotate:
                new_board = board.action(self.board, position = piece.position, rotate=act , direction='No')
            else:
                new_board = board.action(self.board, position = piece.position, rotate='No' , direction=act)
            MCTS_node(board = new_board, parent = self)

        raise NotImplementedError()
    
    def play_random(self):
        # play one random game      
        raise NotImplementedError()
    
    def get_random_move(self):
         
        player = self.board.turn
        if player == config.Player.RED:
            piece_list = self.board.red_pieces
        else: 
            piece_list = self.board.blue_pieces
        
        # Get the alive pieces and make a random choice
        alive_pieces = [piece for piece in piece_list if piece.alive]
        piece_to_move = random.choice(alive_pieces)
        
        
        # Get all possible moves 
        possible_moves = set(r for r in config.Rotate).union(set(m for m in config.Move))
        
        sampled_move = None
        
        while(sampled_move == None): 
            possible_move = random.choice(possible_moves)
            
            # See if the move is legal 
            if possible_move in config.Rotate:
                if board.is_legal_action(self.board, position=piece_to_move.position, direction=None, rotate=possible_move):
                    sampled_move = (None, possible_move)
                    break
            else:
                if board.is_legal_action(self.board, direction=possible_move, rotate=None):
                    sampled_move = (possible_move, None)
                    break
            
            # Else remove that from the set 
            possible_moves.remove(possible_move)
            
        # Return a piece and an action (tuple (direction, rotate)) 
        return piece_to_move, sampled_move
    
    