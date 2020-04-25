import random as r
import numpy

"""
Minesweeper Class:
Functions:
External:
    process_play(x, y):
        returns status, turns
            status - current game state:
                * 0 - game in progress
                * 1 - game lost
                * 2 - game won
            turns - number of player initiated turns
            
    get_known_board():
        returns display_board
            display_board - 2d array [x.y] with with characters at each
            index representing the currently known state of that
            coordinate:
                * '?' - unknown space
                *  0  - 'blank' space
                *  n  - where n is an integer in [1,8] representing the
                        number of adjacent mines


"""


class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        if width <= 1 or height <= 1:
            print("Board must be at least 2x2")
            return 1, 0
        if mines < 1:
            print("There must be at least 1 mine")
            return 1, 0
        self._max_turns = width * height - mines
        if self._max_turns <= 0:
            print("There must be at least 1 safe space")
            return 1, 0
        self._width = width
        self._height = height
        self._mines = mines
        self._board = [[0 for y in range(height)] for x in range(width)]
        self._turns = 0
        self._played_spaces = 0
        self._display_board = [["?" for y in range(height)] for x in range(width)]
        self._training_state = [[100 for y in range(height)] for x in range(width)]

    def generate_mines(self, x, y):
        r.seed()
        for i in range(self._mines):
            rand_x = r.randrange(self._width)
            rand_y = r.randrange(self._height)
            while rand_x == x or rand_y == y or self._board[rand_x][rand_y] == -1:
                rand_x = r.randrange(self._width)
                rand_y = r.randrange(self._height)
            self._board[rand_x][rand_y] = -1

    def minesweep(self, x, y):
        found_mines = 0

        if x < self._width - 1:
            if self._board[x + 1][y] == -1:
                found_mines += 1
            if y < self._height - 1 and self._board[x + 1][y + 1] == -1:
                found_mines += 1
            if y > 0 and self._board[x + 1][y - 1] == -1:
                found_mines += 1
        if x > 0:
            if self._board[x - 1][y] == -1:
                found_mines += 1
            if y < self._height - 1 and self._board[x - 1][y + 1] == -1:
                found_mines += 1
            if y > 0 and self._board[x - 1][y - 1] == -1:
                found_mines += 1
        if y > 0 and self._board[x][y - 1] == -1:
            found_mines += 1
        if y < self._height - 1 and self._board[x][y + 1] == -1:
            found_mines += 1

        self._display_board[x][y] = found_mines
        self._training_state[x][y] = found_mines
        # print("Found {0} mines adjacent to ({1}, {2})".format(found_mines, x, y))

        if found_mines == 0:
            if x < self._width - 1:
                if self._display_board[x + 1][y] == "?":
                    self.minesweep(x + 1, y)
                if y > 0 and self._display_board[x + 1][y - 1] == "?":
                    self.minesweep(x + 1, y - 1)
                if y < self._height - 1 and self._display_board[x + 1][y + 1] == "?":
                    self.minesweep(x + 1, y + 1)
            if x > 0:
                if self._display_board[x - 1][y] == "?":
                    self.minesweep(x - 1, y)
                if y > 0 and self._display_board[x - 1][y - 1] == "?":
                    self.minesweep(x - 1, y - 1)
                if y < self._height - 1 and self._display_board[x - 1][y + 1] == "?":
                    self.minesweep(x - 1, y + 1)
            if y > 0 and self._display_board[x][y - 1] == "?":
                self.minesweep(x, y - 1)
            if y < self._height - 1 and self._display_board[x][y + 1] == "?":
                self.minesweep(x, y + 1)

        self._played_spaces += 1
        return found_mines

    def print_board(self):
        for y in range(self._height - 1, -1, -1):
            for x in range(self._width):
                print(self._display_board[x][y], end="  ")
            print(" ")

    def process_play(self, x, y):
        if self._turns == 0:
            self.generate_mines(x, y)
            self._turns += 1
            found = self.minesweep(x, y)
            self.print_board()
            if self._played_spaces == self._max_turns:
                print("All safe spaces played, you win!")
                return 2, self._turns
            return 0, self._turns
        elif self._board[x][y] == -1:
            print("Mine at ({0},{1})! Game Over!".format(x, y))
            return 1, self._turns + 1
        else:
            found = self.minesweep(x, y)
            self._turns += 1
            self.print_board()
            if self._played_spaces == self._max_turns:
                print("All safe spaces played, you win!")
                return 2, self._turns
            print("Found {0} mines adjacent to ({1}, {2})".format(found, x, y))
            return 0, self._turns

    def training_play(self, y, x):
        y = self._height - y - 1
        if self._turns == 0:
            self.generate_mines(x, y)
            self._turns += 1
            found = self.minesweep(x, y)
            if self._played_spaces == self._max_turns:
                return numpy.array(self._training_state.copy()), 0, 0, 0
            return numpy.array(self._training_state.copy()), 0, 0, 0
        elif self._board[x][y] == -1:
            self._display_board[x][y] = 'X'
            return numpy.array(self._training_state.copy()), -25, 1, self._turns + 1
        elif self._display_board[x][y] != '?':
            return numpy.array(self._training_state.copy()), -10, 0, self._turns
        else:
            old_spaces = self._played_spaces
            found = self.minesweep(x, y)
            self._turns += 1
            # self.print_board()
            if self._played_spaces == self._max_turns:
                print("WIN")
                return numpy.array(self._training_state.copy()), self._height * self._width, 2, self._turns
            reward = (self._played_spaces - old_spaces) * 5
            return numpy.array(self._training_state.copy()), reward, 0, self._turns

    def get_known_board(self):
        return self._display_board.copy()


# new_minesweeper = Minesweeper()
# # new_minesweeper.print_board()
# win, turns = new_minesweeper.process_play(0, 0)
# print(new_minesweeper.get_known_board())
