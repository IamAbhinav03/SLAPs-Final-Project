from z3 import *

def create_sudoku_puzzle(size=9):
    # Create Sudoku puzzle variables
    X = [[Int(f"x_{i}_{j}") for j in range(size)] for i in range(size)]

    # Define Sudoku puzzle constraints
    constraints = [
        # Row constraints
        [Distinct(X[i]) for i in range(size)],
        # Column constraints
        [Distinct([X[i][j] for i in range(size)]) for j in range(size)],
        # Box constraints
        [Distinct([X[i][j] for i in range(3) for j in range(3)]) for k in range(9)],
    ]

    # Add some given numbers to the puzzle
    constraints.append(X[0][0] == 5)
    constraints.append(X[1][1] == 3)
    constraints.append(X[2][2] == 9)

    # Create a Z3 solver instance and add the constraints
    solver = Solver()
    for constraint in constraints:
        solver.add(constraint)

    # Verify the puzzle is solvable
    if solver.check() == sat:
        model = solver.model()
        puzzle = [[model.evaluate(X[i][j]).as_long() for j in range(size)] for i in range(size)]
        return puzzle
    else:
        return None

def verify_sudoku_solution(puzzle, solution):
    # Create Sudoku puzzle variables
    X = [[Int(f"x_{i}_{j}") for j in range(9)] for i in range(9)]

    # Define Sudoku puzzle constraints
    constraints = [
        # Row constraints
        [Distinct(X[i]) for i in range(9)],
        # Column constraints
        [Distinct([X[i][j] for i in range(9)]) for j in range(9)],
        # Box constraints
        [Distinct([X[i][j] for i in range(3) for j in range(3)]) for k in range(9)],
    ]

    # Add the given solution to the constraints
    for i in range(9):
        for j in range(9):
            constraints.append(X[i][j] == solution[i][j])

    # Create a Z3 solver instance and add the constraints
    solver = Solver()
    for constraint in constraints:
        solver.add(constraint)

    # Verify the solution is correct
    if solver.check() == sat:
        return True
    else:
        return False