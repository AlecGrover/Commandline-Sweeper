# Commandline-Sweeper
Basic Minesweeper program for use in a final group project for SFU CMPT-827 Spring 2020.

*Minesweeper.py*:

An importable Minesweeper class, initialize with:

> import Minesweeper as ms 
> game = Minesweeper(width=10, height=10, mines=10)

Default width, height, and number of mines are 10, minimum board size is 2x2 and minimum number of mines is 1. Number of mines must be less than width\*height

To play a space at coordinate (x, y) call:

> game.process_play(x, y)

The class generates a board with a safe first play space when this is called for the first time. *.process_play(x, y)* returns as *state, turns* where state is the current game state as listed below, and the number of turns is the number of calls to *.process_play(x, y)*.

| **State** | **Description** |
|---|---|
| 0 | Game ongoing |
| 1 | Game lost |
| 2 | Game won |

After each call to *.process_play(x, y)* the known board is printed to the command window with '?' representing unknown spaces and numbers representing adjacent mines to explored spaces.

The known board can be retrieved with:

> game.get_known_board()

This returns a 2D array with the same format as the print out, *game.get_known_board()[0]\[0]* is the lower left corner of the print out, and *game.get_known_board()[width - 1]\[height - 1]* is the upper right.

*generate.py*:

Importable function to return a list of lists containing all sets of "offset" tuples for a given *n* neighbors.

Call with:

> get_offsets(n)

Offset tuples are in the format (x, y) where x and y are each in the set [-1, 0, 1] representing the "offset" in that direction of a given space.

*get_offsets* has the additional optional boolean parameters *top*, *bottom*, *left*, and *right*. When set to true in the function call *get_offsets* will only return combinations that do not extend beyond that border.

e.g.

> python generate.py

> \>\>\>get_offsets(3, top=True)

> [((1, 0), (1, -1), (0, -1)), ((1, 0), (1, -1), (-1, -1)), ((1, 0), (1, -1), (-1, 0)), ((1, 0), (0, -1), (-1, -1)), ((1, 0), (0, -1), (-1, 0)), ((1, 0), (-1, -1), (-1, 0)), ((1, -1), (0, -1), (-1, -1)), ((1, -1), (0, -1), (-1, 0)), ((1, -1), (-1, -1), (-1, 0)), ((0, -1), (-1, -1), (-1, 0))]
