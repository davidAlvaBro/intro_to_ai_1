import config

from pieces import King, Switch, Defender, Deflector, Laser
from gui import print_board
import game

from board import Board

board = Board()

snapshot = board.take_snapshot()

# action = dict(position = (4,4), direction = config.Move.UP)

print_board(board)

piece = board.board[4,4].contents

x,y = 4,3

board.board[x,y].contents = None
board.board[x,y-1].contents = piece
piece.position = (x,y-1)

# game.action(board, *action)

print_board(board)

board.restore_from_snapshot(snapshot)

print_board(board)

