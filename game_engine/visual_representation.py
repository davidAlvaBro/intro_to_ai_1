import config
import pieces

# Takes in a board and spits out a visual representation in the console



def print_board(board):
    print("  A B C D E F G H I J")
    for y in range(0, config.HEIGHT):
        print(y+1, end=" ")
        for x in range(0, config.WIDTH):
            cur_field = board.board[(x, y)]
            if cur_field.reserved != None or cur_field.contents != None:
                print(cur_field, end=" ")
            else:
                print(" ", end=" ")
        print()
