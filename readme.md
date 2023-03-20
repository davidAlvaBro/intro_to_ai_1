<!-- omit in toc -->
# Table of Contents

- [Python Laser Chess](#python-laser-chess)
- [How to play](#how-to-play)
- [Implementation](#implementation)
  - [Config](#config)
  - [Game logic](#game-logic)
  - [Graphic Interface](#graphic-interface)
  - [AI](#ai)
  - [Testing files](#testing-files)


# Python Laser Chess
In this repository you'll find the implementation of Laser Chess in Python, made by Group 78 in the course 02180 Introduction to Artificial Intelligence F23.

# How to play
To play the game, run the file `game.py` with Python, and follow the on-screen prompts.

# Implementation
## Config
A lot of various static variables and enums used throughout the whole project are stored in the `config.py` file.
## Game logic
The game logic is implemented in the files `board.py`, `game.py` and `pieces.py`.

## Graphic Interface
The graphical interface for the game have been implemented in `gui.py`.

## AI
All files related to the artificial intelligence are located in the `ai` folder. The file `MCTS.py` implements Monte-Carle Tree Search.
The file `agents.py` implements different agents, using different heuristics for MCTS.

## Testing files
The following files have been used for internal testing and benchmarking, and can be disregarded in regards to the project itself. 

- `generate_stats.py`
- `test_stuff.py`
- `timer.py`
