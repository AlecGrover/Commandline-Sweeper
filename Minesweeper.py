import random as r
from generate import generate_constraints
from dpll import solveDPLL
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
        print("Found {0} mines adjacent to ({1}, {2})".format(found_mines, x, y))

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
            print()

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
            # print("Found {0} mines adjacent to ({1}, {2})".format(found, x, y))
            return 0, self._turns

    def get_known_board(self):
        return self._display_board.copy()

def random_choice(curr_board):
    # choose a random unexplored square in case DPLL fails to find a solution
    ret = []
    for i in range(len(curr_board)):
        row = curr_board[i]
        for j in range(len(row)):
            n = row[j]
            if n == "?":
                ret.append((i,j))
    return ret[r.randint(0, len(ret)-1)]

def getCellIDs(n):
    cords = []
    count = 0
    for i in range(n):
        for j in range(n):
            cords.append([count, i, j])
            count +=1

    print(f'Cordinates: {cords}')
    return cords

def cellIDtoCordinate(cords,target):
    # Conovert into X, Y  cordinates
    res = []
    for cord in cords: 
        if cord[0] == target:
            res = cord

    return(res[1], res[2])


def game_as_CSP(new_minesweeper, winCount, lossCount, size): 
    # Get minesweeper grid
    cords = getCellIDs(size)
    
    # Make first move
    # new_minesweeper = Minesweeper()
    # new_minesweeper.print_board()
    win, turns = new_minesweeper.process_play(0, 0)

    itrCount = 0
    # Game loop
    while(win == 0):
        curr_board = new_minesweeper.get_known_board()
        print(curr_board)

        # Generate clauses
        clauses = generate_constraints(curr_board)
        # VARS = NxN xN 
        VARS = list(range(0,size*size))


        # Call DPLL 
        # Sat: res == True,  Unsat: res == False 
        res, allowedMoves = solveDPLL(VARS, clauses, assignment = [])

        if allowedMoves == []:
            print("UNABLE TO PICK NEXT MOVE --> Choosing a random move!")
            target = random_choice(new_minesweeper.get_known_board())
            target = -1*(target[0]*len(curr_board)+target[1])
        else:
            target = allowedMoves[-1]
        
        print(f'Target:  {target}')


        # Convert cell ID -> grid cordinate
        # using -target because we using Pos SAT assigned values
        mx,my = cellIDtoCordinate(cords, -target)
        print(f'Making Move at cords: {mx},{my}')
        
        # Make next move
        win, turns = new_minesweeper.process_play(mx,my)

        print(f'ITER #: {itrCount}')
        itrCount +=1 

    if win == 2:
        winCount += 1 
    elif win == 1:
        lossCount += 1
    return winCount, lossCount


if __name__ == "__main__":
    winCount = 0
    lossCount = 0
    i = 0
    while i < 10:
        new_minesweeper = Minesweeper()
        winCount, lossCount = game_as_CSP(new_minesweeper, winCount, lossCount)
        i += 1
    print(winCount, lossCount)
