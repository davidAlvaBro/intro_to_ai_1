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


def gui_action_prompt(board):
    print_board(board)
    valid_action = False # Check if we're able to interpret the input as an action
    action = ""
    rotate = ""
    direction = ""
    position = ""
    while not valid_action:
        action = input("Pick your action [Rotate, Move]: ")
        action = action.lower()
        if action == "rotate":
            position, rotate = input("Pick your piece to rotate and rotation direction [Left or Right]: ").split()
        elif action == "move":
            position, direction = input("Pick your piece and direction to move [Up, Right, Down, Left, Right-Up, Right-Down, Left-Up, Left-Down]: ").split()
        else:
            print("Unknown action, try again...")

        if position != "" and (rotate != "" or direction != ""):
            valid_action = True
    
    return position, rotate, direction
