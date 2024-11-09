from z3 import *
from utils.z3_solver import create_sudoku_puzzle, verify_sudoku_solution


def sudoku_puzzle():
    puzzle = create_sudoku_puzzle()
    if puzzle:
        print("Sudoku Puzzle:")
        for row in puzzle:
            print(row)
        solution = input("Enter your solution (space-separated rows): ")
        solution = [list(map(int, row.split())) for row in solution.split(";")]
        if verify_sudoku_solution(puzzle, solution):
            print("Correct solution!")
            return True
        else:
            print("Incorrect solution. Try again!")
            return False
    else:
        print("Failed to generate Sudoku puzzle.")
        return None
