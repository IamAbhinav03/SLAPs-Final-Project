from z3 import *

def create_sudoku_constraints():
    # Define a 9x9 Sudoku grid with variables from 1 to 9
    grid = [[Int(f"cell_{i}_{j}") for j in range(9)] for i in range(9)]
    print(grid)

    # Define the Sudoku constraints
    constraints = []

    # Row constraints
    for i in range(9):
        constraints.append(Distinct(grid[i]))  # Each row should have distinct values

    # Column constraints
    for j in range(9):
        constraints.append(Distinct([grid[i][j] for i in range(9)]))  # Each column should have distinct values

    # 3x3 subgrid constraints
    for i in range(3):
        for j in range(3):
            constraints.append(Distinct([grid[i*3 + di][j*3 + dj] for di in range(3) for dj in range(3)]))

    # Non-linear constraints (example: sum of cells in a certain range must be a specific number)
    constraints.append(Sum([grid[i][j] for i in range(3) for j in range(3)]) == 15)
    # The sum of all cells in the middle 3x3 subgrid must equal 45
    constraints.append(Sum([grid[i][j] for i in range(3, 6) for j in range(3, 6)]) == 45)

    # The product of cells in the first row must equal 720 (i.e., 1*2*3*4*5*6*7*8*9)
    # constraints.append(Product([grid[0][j] for j in range(9)]) == 720)

    return grid, constraints

def solve_sudoku():
    # Create Sudoku constraints
    grid, constraints = create_sudoku_constraints()

    # Solve the problem using Z3
    solver = Solver()
    solver.add(constraints)

    if solver.check() == sat:
        model = solver.model()
        solved_grid = [[model[cell].as_long() for cell in row] for row in grid]
        return solved_grid
    else:
        return None

solved_sudoku = solve_sudoku()
print(solved_sudoku)

import pygame

def draw_grid(screen, solved_sudoku):
    font = pygame.font.Font(None, 40)
    for i in range(9):
        for j in range(9):
            rect = pygame.Rect(j * 60, i * 60, 60, 60)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            if solved_sudoku:
                text = font.render(str(solved_sudoku[i][j]), True, (0, 0, 0))
                screen.blit(text, (j * 60 + 20, i * 60 + 20))

def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 540))
    pygame.display.set_caption('SAT Solver Sudoku')

    # Solve the Sudoku puzzle
    solved_sudoku = solve_sudoku()

    # Main game loop
    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_grid(screen, solved_sudoku)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()