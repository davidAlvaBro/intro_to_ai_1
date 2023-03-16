import config

from pieces import King, Switch, Defender, Deflector, Laser
from gui import print_board
import game

from board import Board

board = Board()

snapshot = board.take_snapshot()


def modify_board(board):
# action = dict(position = (4,4), direction = config.Move.UP)


    piece = board.board[4,3].contents


    board.board[4,2].contents = piece
    board.board[4,3].contents = None
    piece.position = 4,2

    return board

def print_laser(board: Board):
    for p in board.red_pieces:
        if isinstance(p, Laser):
            print(p.position, "red")
    for p in board.blue_pieces:
        if isinstance(p, Laser):
            print(p.position, "blue")

print_board(board)
mod_baord = modify_board(board)
print_board(board)
print_laser(board)
board.restore_from_snapshot(snapshot)
print_laser(board)
print_board(board)