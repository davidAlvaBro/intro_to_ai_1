import config 
import board as b
import random

class simple_agent: 
    def random_move(self, board: b.Board):
        """
        Get a random legal move in the current board state 
        """
        
        player = board.turn
        if player == config.Player.RED:
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

    def stationary_move(self, board: b.Board):
        """
        Rotate the king (which essentially does nothing)
        """
        
        player = board.turn
        if player == config.Player.RED:
            piece_list = board.red_pieces
        else: 
            piece_list = board.blue_pieces
        
        # Find the king 
        for piece in piece_list: 
            if piece.piece == "King": 
                piece_to_move = piece
        
        return piece_to_move.position, (None, config.Rotate.LEFT)
