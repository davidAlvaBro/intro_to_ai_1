from ..ame_engine..oard import Board
"""
input: board


architecture:



do:
a := get legal actions
make dead/alive lists 
for each legal action:


"""

class MCTS_node: 
    def __init__(self, board: , parent) -> None:
        self.snapshot = board. 
        self.board = board
        self.won_games = 0
        self.total_games = 0
        self.children = {} # key : piece_action = (pos, action) , value : node 
        self.UCB = None
        self.play_random() 
        # Save snapshot 
        # Do play random while restore from snapshot play random X times 
    
    def backprop(self, n_won, n_lost):
        
    
    def expand(self):
        # Generate all legal actions
        # For each action generate child with correct board (restore snapshot first)
        raise NotImplementedError()
    
    def play_random(self):
        # play one random game      
        
    
    