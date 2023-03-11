from enum import Enum
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

WIDTH = 10
HEIGHT = 8


class Player(Enum):
    NONE = 0
    BLUE = 1 
    RED = -1
    
    def change_player(self):
        return Player(-1*self.value)

class Rotate(Enum):
    LEFT = 0
    RIGHT = 1
    
    # TODO make a function that takes in orientation and spits out orientation 

class Move(Enum):
    UP = (0,-1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT_UP = (1, -1)
    RIGHT_DOWN = (1, 1)
    LEFT_DOWN = (-1, 1)
    LEFT_UP = (-1, -1)
      

class Orientation(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    def toMove(self):
        if self == Orientation.UP: 
            return Move.UP
        elif self == Orientation.DOWN: 
            return Move.DOWN
        elif self == Orientation.LEFT: 
            return Move.LEFT
        elif self == Orientation.RIGHT: 
            return Move.RIGHT
        else: 
            raise ValueError("DUM NUMS")


class LaserOptions(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    DEAD = 4 
    STOP = 5 
    
    def toMove(self):
        if self == LaserOptions.UP: 
            return Move.UP
        elif self == LaserOptions.DOWN: 
            return Move.DOWN
        elif self == LaserOptions.LEFT: 
            return Move.LEFT
        elif self == LaserOptions.RIGHT: 
            return Move.RIGHT
        else: 
            raise ValueError("DUM NUMS")


def print_blue(symbol):
    print(f"{Fore.BLUE}{symbol}{Style.RESET_ALL}", end=" ")

def print_red(symbol):
    print(f"{Fore.RED}{symbol}{Style.RESET_ALL}", end=" ")

def blue_piece(symbol):
    return Fore.BLUE+symbol+Style.RESET_ALL

def red_piece(symbol):
    return Fore.RED+symbol+Style.RESET_ALL
    
# TODO Have laser position in here 
laser_position = (None, None)