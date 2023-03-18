# from game_engine import config
# from game_engine import board
# from game_engine.config import Player as p
import config
import board
from config import Player as p
import random
import math
from tqdm import tqdm


class MCTS_node: 
    def __init__(self, board: board.Board, parent, optimize_player = config.AI_PLAYER) -> None:
        """
        board is the board - the node will take a snapshot of the state of the given board
        parent is the parent MCTS Node
        optimize_player is the player that we are optimizing for, so either Player.RED or Player.BLUE

        """

        self.optimize_player = optimize_player
        self.board = board
        self.snapshot = board.take_snapshot()
        self.won = self.snapshot["won"]
        self.turn = self.snapshot["turn"]
        self.parent: MCTS_node = parent
        self.children = {} # key : piece_action = (pos, action) , value : node 
        self.won_games = 0
        self.total_games = 0
    
    def __repr__(self):
        return f"Node(turn={self.turn}, winner={self.won}, {self.won_games}, {self.total_games}, {self.LCB}, {self.UCB})"

    def get_best_child(self, reverse=False):
        """
        returns the best child and the action leading to it.
        """
        if self.won is p.NONE and len(self.children) > 0:
            UCB = lambda x: self.children[x].UCB
            LCB = lambda x: self.children[x].LCB
            if (self.optimize_player == self.turn):
                choose_fn = max
                if not reverse: key_fn = UCB
                else:           key_fn = LCB
            else:
                choose_fn = min
                if not reverse: key_fn = LCB
                else:           key_fn = UCB

            position, action = choose_fn(self.children.keys(), key=key_fn)
            return position, action, self.children[(position, action)]

    # def play_N_random(self, N):
    #     for i in range(N):
    #         if i != 0: self.board.restore_from_snapshot(self.snapshot)
    #         self.won_games += self.play_random()
    #     self.total_games += N
    
    @property
    def UCB(self):
        return self.get_confidence_bounds()[1]
    @property
    def LCB(self):
        return self.get_confidence_bounds()[0]

    def get_confidence_bounds(self):
        """
        return LCB, UCB
        """
        if self.total_games == 0:
            return None, None
        elif self.won is p.NONE:
            a = self.won_games/self.total_games
            b = math.sqrt(2*math.log(self.parent.total_games)/self.total_games)
            # b = (1-a)*a/self.total_games*1.96
            return a - b, a + b
        elif self.won == self.optimize_player:
            return float("inf"), float("inf")
        else:
            return float("-inf"), float("-inf")

    def backprop(self, n_won, n_total):
        node = self
        while node is not None:
            node.won_games += n_won
            node.total_games += n_total
            node = node.parent

    
    def expand(self):
        # Generate all legal actions
        # For each action generate child with correct board (restore snapshot first)
        
        # Prepare to expand - restore from snapshot and get legal actions
        N = config.INITIAL_RANDOM_GAMES

        if self.won != p.NONE:
            n_won = int(self.won == self.optimize_player)*N
            n_total = N

        else:
            self.board.restore_from_snapshot(self.snapshot)
            legal_actions = board.get_legal_actions(self.board)
            # For each action make the child
            n_won = 0
            n_total = 0
            for i, (piece, act) in enumerate(legal_actions):
                # restore from snapshot
                if i != 0: self.board.restore_from_snapshot(self.snapshot)
                # take action
                board.step(self.board, position=piece.position, rotate=act[1], direction=act[0])
                child = MCTS_node(board=self.board, parent=self)
                # test if the game is over
                if child.won != p.NONE:
                    # if the game is over, just pretend that the child played N games and won N games if the child won the game
                    child.won_games = int(child.won == child.optimize_player)*N
                    child.total_games = N
                else:
                    #play N random games
                    for j in range(N):
                        # if j != 0: child.board.restore_from_snapshot(self.snapshot)
                        self.won_games += self.play_random(restore_from_snapshot = (j != 0))
                        self.total_games += 1
                n_won += child.won_games
                n_total += child.total_games
                self.children[(piece.position, act)] = child

        return n_won, n_total
        # self.backprop(n_won, n_total)

        
    
    def play_random(self, restore_from_snapshot = True):
        """Plays a random game from the board position at self.board
        
        return:
            Player that won 
        """
        # TODO maybe limit the maximal number of iterations
        depth = 0
        if restore_from_snapshot: self.board.restore_from_snapshot(self.snapshot)
        while depth < config.MAX_RANDOM_DEPTH:
            depth += 1
            if depth%1000 == 0: print("monte carlo depth reached",depth)
            # Get a random move - It is legal 
            piece, action = self.get_random_move()
            
            # Move 
            board.step(self.board, piece.position, direction=action[0], rotate=action[1])

            # Goal test 
            if board.goal_test(self.board): 
                break 
        
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
        # possible_moves = set(r for r in config.Rotate).union(set(m for m in config.Move))
        possible_moves = [r for r in config.Rotate] + [m for m in config.Move]
        n_possible = len(possible_moves)
        
        sampled_move = None
        
        while(sampled_move == None): 
            idx = random.randint(0, n_possible-1)
            possible_move = possible_moves[idx]
            
            # See if the move is legal 
            if possible_move in config.Rotate:
                if board.is_legal_action(self.board, position=piece_to_move.position, direction=None, rotate=possible_move):
                    sampled_move = (None, possible_move)
                    break
            else:
                if board.is_legal_action(self.board, position=piece_to_move.position, direction=possible_move, rotate=None):
                    sampled_move = (possible_move, None)
                    break
            
            # Else remove that from the set
            possible_moves[idx] = possible_moves[n_possible-1]
            n_possible -= 1
            assert n_possible > 0, "No legal moves"
            
        # Return a piece and an action (tuple (direction, rotate)) 
        return piece_to_move, sampled_move


def select_expansion_node(root: MCTS_node) -> MCTS_node:
    """Selects the best node to expand
    
    Args:
        node (MCTS_node): The node to expand
    
    Returns:
        MCTS_node: The best node to expand
    """
    while len(root.children) != 0:
        position, action, root = root.get_best_child()
    return root


def print_tree(root, layer=0):
    print("   "*layer, root)
    for (pos, act), child in root.children.items():
        assert pos is not None and act is not None
        print_tree(child, layer+1)
    

def run_monte_carlo(board: board.Board, N: int, return_diagnostics=False) -> tuple:
    """Runs the Monte Carlo Tree Search algorithm
    
    Args:
        board (Board): The board to run the algorithm on
        N (int): Number of iterations
    
    Returns:
        tuple: (piece, action) - the best move
    """
    root = MCTS_node(board, None)
    for i in tqdm(range(N), desc="Running Monte Carlo Tree Search"):
        node = select_expansion_node(root)
        n_won, n_total = node.expand()
        node.backprop(n_won, n_total)
    (position, (rotate, direction), child), root = root.get_best_child(reverse=True)
    if return_diagnostics:
        return position, rotate, direction, child, root
    else:
        return position, rotate, direction

if __name__ == "__main__":
    b = board.Board()
    (position, action, child), root = run_monte_carlo(b, 100)
    for c in root.children.values():
        print(c)
    print(f"Best move is\n  postition:{position}\n  action:{action}\n  with {child.won_games} wins out of {child.total_games} games")