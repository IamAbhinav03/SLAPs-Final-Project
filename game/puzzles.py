from z3 import Solver, Int, Distinct, Or
import random

def generate_sudoku():
    """
    Generates a Sudoku puzzle with a unique solution.
    Returns a tuple of (puzzle, solution).
    """
    def fill_grid(grid):
        """Fills the grid with a complete solution."""
        solver = Solver()
        cells = [[Int(f'cell_{i}_{j}') for j in range(9)] for i in range(9)]

        # Constraints for cells
        for i in range(9):
            for j in range(9):
                solver.add(cells[i][j] >= 1, cells[i][j] <= 9)

        # Row constraints
        for i in range(9):
            solver.add(Distinct(cells[i]))

        # Column constraints
        for j in range(9):
            solver.add(Distinct([cells[i][j] for i in range(9)]))

        # 3x3 sub-grid constraints
        for box_row in range(3):
            for box_col in range(3):
                solver.add(Distinct([cells[i][j]
                                     for i in range(box_row * 3, box_row * 3 + 3)
                                     for j in range(box_col * 3, box_col * 3 + 3)]))

        # Solve the puzzle
        if solver.check() == 'sat':
            model = solver.model()
            for i in range(9):
                for j in range(9):
                    grid[i][j] = model[cells[i][j]].as_long()

    # Generate a full grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    fill_grid(grid)

    # Save the solution
    solution = [row[:] for row in grid]

    # Remove some numbers to create a puzzle
    for _ in range(random.randint(40, 50)):  # Remove 40-50 numbers
        i, j = random.randint(0, 8), random.randint(0, 8)
        while grid[i][j] == 0:  # Ensure we only remove already filled cells
            i, j = random.randint(0, 8), random.randint(0, 8)
        grid[i][j] = 0

    return grid, solution


def solve_sudoku(puzzle):
    """
    Solves a given Sudoku puzzle using the Z3 solver.
    Returns the solved grid.
    """
    solver = Solver()
    cells = [[Int(f'cell_{i}_{j}') for j in range(9)] for i in range(9)]

    # Constraints for cells
    for i in range(9):
        for j in range(9):
            solver.add(cells[i][j] >= 1, cells[i][j] <= 9)

    # Row constraints
    for i in range(9):
        solver.add(Distinct(cells[i]))

    # Column constraints
    for j in range(9):
        solver.add(Distinct([cells[i][j] for i in range(9)]))

    # 3x3 sub-grid constraints
    for box_row in range(3):
        for box_col in range(3):
            solver.add(Distinct([cells[i][j]
                                 for i in range(box_row * 3, box_row * 3 + 3)
                                 for j in range(box_col * 3, box_col * 3 + 3)]))

    # Add known values from the puzzle
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                solver.add(cells[i][j] == puzzle[i][j])

    # Solve the puzzle
    if solver.check() == 'sat':
        model = solver.model()
        solved_grid = [[model[cells[i][j]].as_long() for j in range(9)] for i in range(9)]
        return solved_grid
    else:
        raise ValueError("No solution exists for the given puzzle.")


def get_hint(puzzle, user_grid, solution):
    """
    Provides a hint for the Sudoku puzzle by comparing the user's grid with the solution.
    Finds the first cell where the user has not filled in a number.
    """
    for i in range(9):
        for j in range(9):
            if user_grid[i][j] == 0:  # Empty cell
                return f"Try placing {solution[i][j]} in row {i+1}, column {j+1}."
    return "The grid is already complete!"


# Example for testing
if __name__ == "__main__":
    puzzle, solution = generate_sudoku()
    print("Puzzle:")
    for row in puzzle:
        print(row)
    print("\nSolution:")
    for row in solution:
        print(row)

    print("\nTesting solver...")
    solved_grid = solve_sudoku(puzzle)
    for row in solved_grid:
        print(row)