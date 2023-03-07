import config
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

# Takes in a board and spits out a visual representation in the console

def print_blue(symbol):
    print(f"{Fore.BLUE}{symbol}{Style.RESET_ALL}", end=" ")

def print_red(symbol):
    print(f"{Fore.RED}{symbol}{Style.RESET_ALL}", end=" ")

def print_board(board):
    print(" ", end=" ")
    for x in range(0, config.WIDTH):
        print("?", end=" ")
        # TODO - Print remaining rows in board 