from game_engine import config
from game_engine import board
from game_engine.config import Player
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
    def __init__(self, board: board.Board, parent, optimize_player) -> None:
        """
        board is the board - the node will take a snapshot of the board itself
        parent is the parent MCTS Node
        optimize_player is the player that we are optimizing for, so either Player.RED or Player.BLUE

        """
        self.optimize_player = optimize_player
        self.board = board
        self.snapshot = board.take_snapshot()
        self.parent: MCTS_node = parent
        self.children = {} # key : piece_action = (pos, action) , value : node 
        self.UCB = None
        self.LCB = None
        self.won_games = 0
        self.total_games = 0
    
    def get_best_child(self):
        if self.optimize_player == self.snapshot["turn"]:
            return max(self.children.values(), key=lambda x: x.UCB)
        else:
            return min(self.children.values(), key=lambda x: x.LCB)
        
    def play_N_random(self, N):
        n_won = 0
        for i in range(N):
            if i != 0: self.board.restore_from_snapshot(self.snapshot)
            n_won += self.play_random()
        self.update_game_counters(n_won, N)
    
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
        
        # Prepare to expand - restore from snapshot and get legal actions
        self.board.restore_from_snapshot(self.snapshot)
        legal_actions = board.get_legal_actions(self.board)
        N = config.INITIAL_GAMES
        # For each action make the child
        n_won = 0
        n_total = 0
        for i, (piece, act) in enumerate(legal_actions):
            # restore from snapshot
            if i != 0: self.board.restore_from_snapshot(self.snapshot)
            # take action
            board.action(self.board, position=piece.position, rotate=act[1], direction=act[0])
            child = MCTS_node(board=self.board, parent=self)
            # test if the game is over
            if self.board.won != Player.NONE:
                # if the game is over, just pretend that the child played N games and won N games if the child won the game
                child.update_game_counters(int(self.board.won == self.optimize_player)*N, N)
            else:
                child.play_N_random(N)
            n_won += child.won_games
            n_total += child.total_games
            self.children[(piece.position, act)] = child
        self.backprop(n_won, n_total)

        
    
    def play_random(self):
        """Plays a random game from the board position at self.board
        
        return:
            Player that won 
        """
        # TODO maybe limit the maximal number of iterations
        while(True): 
            # Get a random move - It is legal 
            piece, action = self.get_random_move()
            
            # Move 
            self.board = board.step(self.board, piece.position, direction=action[0], rotate=action[1]) # TODO is the "self.board =" necessary? if it is we use much more space  
            
            # Goal test 
            if board.goal_test(self.board): 
                break 
        
        #return self.board.won # TODO To return 0 and 1 we need to know which player is controlling the MCST, for now assume that the computer is always RED 
        return int(self.board.won == self.optimize_player) # This is to make it a 1 or 0
        
    
    def get_random_move(self):
        """Function that returns a random action in the board position (stored in self)

        Returns:
            piece_to_move (Piece): The chosen piece to move 
            sampled_move (tuple): (Move, Rotate) - one element is None
        """
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


def select_node(node: MCTS_node) -> MCTS_node:
    """Selects the best node to expand
    
    Args:
        node (MCTS_node): The node to expand
    
    Returns:
        MCTS_node: The best node to expand
    """
    while len(node.children) != 0:#TODO check if game is done
        node = node.get_best_child()
    return node

def run_monte_carlo(board: board.Board, N: int) -> tuple:
    """Runs the Monte Carlo Tree Search algorithm
    
    Args:
        board (Board): The board to run the algorithm on
        N (int): Number of iterations
    
    Returns:
        tuple: (piece, action) - the best move
    """
    root = MCTS_node(board, None)
    for i in range(N):
        pass # TODO