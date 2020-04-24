import time 
import generate
from Minesweeper import Minesweeper, game_as_CSP
import argparse

def averageList(nums):
    sums = 0
    for i in nums:
        sums = sums + i 
    avg = sums / len(nums)    
    return avg


def test(n, s, m):
    lossCount_CSP = 0
    winCount_CSP = 0 

    start = time.time()
    # Run tests
    i = 0
    while i < n:
        # Create the Minesweeper (both for CSP and RL)
        new_minesweeper = Minesweeper(width=s, height=s, mines=m)
        winCount_CSP, lossCount_CSP = game_as_CSP(new_minesweeper, winCount_CSP, lossCount_CSP, s)
        i += 1
    end = time.time()
    overall_time = end - start
    print("\n\n")
    print("Results of running CSP on {} puzzles: \n".format(n))
    print("CSP success rate: {}".format(winCount_CSP/n))
    print("CSP avg game time: {}".format(overall_time/n))


if __name__ == "__main__":
    # add a command line argument
    parser = argparse.ArgumentParser(description='Comparing performance of CSP vs. RL')
    parser.add_argument('-n', help='number of games to test on', type=int, default=10)
    parser.add_argument('-s', help='size of the minesweeper', type=int, default=10)
    parser.add_argument('-m', help='number of mines', type=int, default=10)
    args = parser.parse_args()
    
    test(args.n, args.s, args.m)