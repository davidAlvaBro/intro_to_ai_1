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

def input_to_direction(input_text) -> config.Move: 
    input_text.upper()
    # TODO Maybe moving wrong place. Ex it moved Left-Down instead of Down.
    if input_text not in ("UP", "DOWN", "LEFT", "RIGHT"):
        if input_text == "RIGHT-UP":
            input_text = "RIGHT_UP"
        elif input_text == "RIGHT-DOWN":
            input_text = "RIGHT_DOWN"
        elif input_text == "LEFT-UP":
            input_text = "LEFT_UP"
        else: 
            input_text = "LEFT_DOWN"
    return config.Move[input_text]

def input_to_tuple(input_text):
    x = ord(input_text[0]) - ord('A')
    y = ord(input_text[1]) - ord('1')
    return (x,y)

def input_to_rotate(input_text):
    return config.Rotate[input_text.upper()]


def gui_action_prompt(board):
    print_board(board)
    valid_action = False # Check if we're able to interpret the input as an action
    action = ""
    rotate = None
    direction = None
    position = None
    while not valid_action:
        action = input("Pick your action [Rotate, Move]: ")
        action = action.lower()
        # TODO Error handling if user doesn't pass enough inputs for input function to unpack
        if action == "rotate":
            position, rotate = input("Pick your piece to rotate, ex. A3, and rotation direction, Left or Right: ").split(' ')
            position = input_to_tuple(position)
            rotate = input_to_rotate(rotate)
        elif action == "move":
            position, direction = input("Pick your piece and direction to move [Up, Right, Down, Left, Right-Up, Right-Down, Left-Up, Left-Down]: ").split()
            position = input_to_tuple(position)
            direction = input_to_direction(direction)
        else:
            print("Unknown action, try again...")

        if position is not None and (rotate is not None or direction is not None):
            valid_action = True
    
    return position, rotate, direction

def gui_illegal_action():
    print("Attempted action was illegal, try again...")

def gui_announce_winner(board):
    print(f"The game has finished, the winner is the {board.turn.name.title()} player!")
