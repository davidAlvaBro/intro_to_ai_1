# from game_engine import config
# from game_engine import board
# from game_engine.config import Player as p
import config
import board
from config import Player as p
import random
import math
from pieces import Piece, Laser
from tqdm import tqdm
from typing import List, Tuple, Dict, Union
# import Iterable
from collections.abc import Iterable
from gui import print_board


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
        self.total_reward = 0
        self.total_games = 0
    
    def __repr__(self):
        return f"Node(turn={self.turn}, winner={self.won}, {self.total_reward}, {self.total_games}, {self.LCB}, {self.UCB})"

    def get_best_child(self, select_for_action=False):
        """
        returns the best child and the action leading to it.
        """
        # TODO is the if statement necessary
        if self.won is p.NONE and len(self.children) > 0:
            # Depending on whether we are selecting for action or not, we use UCB/LCB or total games
            # And if we are currently searching in the tree we want to maximize or minimize the UCB/LCB depending on the player
            UCB = lambda x: self.children[x].UCB
            LCB = lambda x: self.children[x].LCB
            total_games = lambda x: self.children[x].total_games
            if select_for_action: # Max games to make action
                choose_fn = max
                key_fn = total_games
            elif (self.optimize_player == self.turn): # Max UCB to find most promising node for the ai player
                choose_fn = max
                key_fn = UCB
            else: # Min LCB to find most promising node for the opponent
                choose_fn = min
                key_fn = LCB

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
    @property
    def mean(self):
        return self.get_confidence_bounds()[2]

    def get_confidence_bounds(self):
        """
        return LCB, UCB
        """
        if self.total_games == 0 or self.parent.total_games == 0:
            return None, None
        elif self.won is p.NONE:
            a = self.total_reward/self.total_games
            b = math.sqrt(2*math.log(self.parent.total_games)/self.total_games)
            # b = (1-a)*a/self.total_games*1.96
            return a - b, a + b, a
        elif self.won == self.optimize_player:
            return float("inf"), float("inf"), float('inf')
        else:
            return float("-inf"), float("-inf"), float('-inf')

    def backprop(self, n_won, n_total):
        node = self
        while node is not None:
            node.total_reward += n_won
            node.total_games += n_total
            node = node.parent

    def compute_reward(self, won, turn):
        # Destinguish between active and passive player victories
        if won == self.optimize_player: sign = 1
        else:                           sign = -1
        if turn != won: score = 2
        else:           score = 1
        return sign*score/2


    def expand(self, guided, initial_random_games=config.INITIAL_RANDOM_GAMES):
        # Generate all legal actions
        # For each action generate child with correct board (restore snapshot first)
        
        # Prepare to expand - restore from snapshot and get legal actions
        N = initial_random_games

        if self.won != p.NONE:
            total_reward = int(self.won == self.optimize_player)*N
            total_games = N

        else:
            self.board.restore_from_snapshot(self.snapshot)
            legal_actions = board.get_legal_actions(self.board)
            # For each action make the child
            total_reward = 0
            total_games = 0
            for i, (position, act) in enumerate(legal_actions):
                assert position is not None
                assert act is not None
                # assert pos is not None and act is not None
                # restore from snapshot
                if i != 0: self.board.restore_from_snapshot(self.snapshot)
                # take action
                board.step(self.board, position=position, rotate=act[1], direction=act[0])
                child = MCTS_node(board=self.board, parent=self, optimize_player=self.optimize_player)
                # test if the game is over
                if child.won != p.NONE:
                    # if the game is over, just pretend that the child played N games and won N games if the child won the game
                    child.total_games = N
                    child.total_reward = child.compute_reward(child.won, child.turn.change_player()) # new version
                else:
                    #play N random games
                    for j in range(N):
                        # if j != 0: child.board.restore_from_snapshot(self.snapshot)
                        child.total_reward += child.play_random(restore_from_snapshot = (j != 0), guided=guided)
                        child.total_games += 1
                total_reward += child.total_reward
                total_games  += child.total_games
                self.children[(position, act)] = child
                assert position is not None
                assert act is not None

        return total_reward, total_games
        # self.backprop(n_won, n_total)

        
    
    def play_random(self, restore_from_snapshot = True, guided=True):
        """Plays a random game from the board position at self.board
        
        return:
            Player that won 
        """
        # TODO maybe limit the maximal number of iterations
        depth = 0
        if restore_from_snapshot: self.board.restore_from_snapshot(self.snapshot)
        while depth < config.MAX_RANDOM_DEPTH:
            depth += 1
            # if depth%1000 == 0: print("monte carlo depth reached", depth)
            # Get a random move - It is legal 

            for chosen_piece, action in self.get_random_move():
                chosen_piece_snapshot = chosen_piece.take_snapshot()
                # Move 
                _, killed_piece, killed_piece_snapshot = board.step(self.board, chosen_piece.position, direction=action[0], rotate=action[1])
                if not guided:
                    found_move = True
                    break

                # check if killed piece is opponent piece or none
                if killed_piece is None or killed_piece.player == self.board.turn:
                    found_move = True
                    break
                else:
                    found_move = False
                    # reverse the move
                    # change the turn
                    self.board.turn = self.board.turn.change_player()
                    self.board.won = p.NONE

                    # reverse the move (piece)
                    if chosen_piece.position is not None:
                        self.board.board[chosen_piece.position].contents = None
                    chosen_piece.restore_from_snapshot(chosen_piece_snapshot)
                    self.board.board[chosen_piece.position].contents = chosen_piece

                    # revive the killed piece
                    if killed_piece is not None and killed_piece != chosen_piece:
                        killed_piece.restore_from_snapshot(killed_piece_snapshot)
                        self.board.board[killed_piece.position].contents = killed_piece

                    

            # Goal test 
            if board.goal_test(self.board) or not found_move:
                break 

        if found_move: # Return the reward of the
            return self.compute_reward(self.board.won, self.board.turn)
        else:
            return 0
        
    
    def get_random_move(self):
        """Function that returns a random action in the board position (stored in self)

        Returns:
        iterator over legal actions in random order
        implemented as a generator, so it only calculates the next action when needed
            yields tuples of:
                piece_to_move (Piece): The chosen piece to move 
                sampled_move (tuple): (Move, Rotate) - one element is None
        """
        player = self.board.turn
        if player == config.Player.RED: piece_list = self.board.red_pieces
        else:                           piece_list = self.board.blue_pieces
        
        # Get the alive pieces and make a random choice
        piece_idxs = random.sample(range(len(piece_list)), k=len(piece_list))
        
        for piece_idx in piece_idxs:
            # Get a random piece
            piece_to_move = piece_list[piece_idx]
            if piece_to_move.alive == False: continue
            
            # Get all possible moves 
            # possible_moves = set(r for r in config.Rotate).union(set(m for m in config.Move))
            possible_moves = [r for r in config.Rotate] + [m for m in config.Move]
            possible_moves = random.sample(possible_moves, k=len(possible_moves))
            
            sampled_move = None
            
            for possible_move in possible_moves:
                
                # See if the move is legal 
                if possible_move in config.Rotate:
                    if board.is_legal_action(self.board, position=piece_to_move.position, direction=None, rotate=possible_move):
                        sampled_move = (None, possible_move)
                else:
                    if board.is_legal_action(self.board, position=piece_to_move.position, direction=possible_move, rotate=None):
                        sampled_move = (possible_move, None)
                
                if sampled_move is not None:
                    # Yields a piece and an action (tuple (direction, rotate))
                    yield piece_to_move, sampled_move

        
        # return piece_to_move, sampled_move


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


def print_tree(root, pos=None, act=None, layer=0):
    print("   "*layer, pos, act, root)
    for (pos, act), child in root.children.items():
        # assert pos is not None and act is not None
        print_tree(child, pos, act, layer+1)
    
def print_action(pos, rotate, direction):
    x = chr(pos[0] + ord('A'))
    y = pos[1] + 1
    if rotate is not None: act = "rotate", rotate.name
    else:                  act = "move", direction.name
    return f"{act[0]} {x}{y} {act[1]}"


def run_monte_carlo(board: board.Board,
                    initial_random_games = config.INITIAL_RANDOM_GAMES,
                    mc_n_iterations = config.MC_N_ITERATIONS,
                    guided=True,
                    optimize_player=config.AI_PLAYER) -> tuple:
    """
    Runs the Monte Carlo Tree Search algorithm
    
    Args:
        board (Board): The board to run the algorithm on
        N (int): Number of iterations

    Returns:
        tuple: (piece, action) - the best move
    """
    root = MCTS_node(board, None, optimize_player=optimize_player)
    for i in tqdm(range(mc_n_iterations), desc="Running Monte Carlo Tree Search"):
        node = select_expansion_node(root)
        n_won, n_total = node.expand(guided, initial_random_games)
        node.backprop(n_won, n_total)
    position, (direction, rotate), child = root.get_best_child(select_for_action=True)
    board.restore_from_snapshot(root.snapshot)
    return position, rotate, direction, root, child

if __name__ == "__main__":
    b = board.Board()
    position, action, child, root, child = run_monte_carlo(b, 100, True)
    for c in root.children.values():
        print(c)
    print(f"Best move is\n  postition:{position}\n  action:{action}\n  with {child.total_reward} wins out of {child.total_games} games")
    # print(timer)