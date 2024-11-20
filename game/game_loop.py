import pygame
from pygame.locals import *
from .story import prompt_graph, INTRO, DAY_1  # Story remains the same
from .puzzles import generate_sudoku, solve_sudoku  # Import functions to generate and solve Sudoku
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE, BLACK, GRAY, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (200, 200, 200), (255, 0, 0), (0, 255, 0), (0, 0, 255)
FONT = pygame.font.Font(None, 36)
CELL_SIZE = 50
GRID_OFFSET = 100

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Logic Island Survival")

def render_text(text, y, font_size=36, color=BLACK):
    """Helper function to render multi-line text on the screen."""
    font = pygame.font.Font(None, font_size)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        rendered_line = font.render(line, True, color)
        screen.blit(rendered_line, (20, y + i * (font_size + 5)))

def render_choices(choices, y):
    """Helper function to render numbered choices."""
    for i, choice in enumerate(choices):
        choice_text = FONT.render(f"{i + 1}. {choice}", True, BLACK)
        screen.blit(choice_text, (20, y + i * 40))

def draw_sudoku(puzzle, user_grid):
    """Draw the Sudoku puzzle grid."""
    for row in range(9):
        for col in range(9):
            x = GRID_OFFSET + col * CELL_SIZE
            y = GRID_OFFSET + row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE if puzzle[row][col] == 0 else GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            # Render numbers
            if puzzle[row][col] != 0:  # Pre-filled numbers in the puzzle
                num_text = FONT.render(str(puzzle[row][col]), True, BLUE)
                screen.blit(num_text, (x + 15, y + 10))
            elif user_grid[row][col] != 0:  # User-filled numbers
                num_text = FONT.render(str(user_grid[row][col]), True, GREEN)
                screen.blit(num_text, (x + 15, y + 10))

def sudoku_puzzle():
    """Play the Sudoku puzzle using Pygame."""
    # Generate Sudoku puzzle and solve it
    puzzle, solution = generate_sudoku()  # Function to create a Sudoku puzzle
    user_grid = [[puzzle[row][col] for col in range(9)] for row in range(9)]

    selected_cell = [0, 0]

    while True:
        screen.fill(WHITE)
        render_text("Solve the Sudoku Puzzle (Press H for Zelta's help):", 20)
        draw_sudoku(puzzle, user_grid)

        # Highlight the selected cell
        x = GRID_OFFSET + selected_cell[1] * CELL_SIZE
        y = GRID_OFFSET + selected_cell[0] * CELL_SIZE
        pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE), 3)

        render_text("Press Enter to Submit or Esc to Quit", SCREEN_HEIGHT - 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False  # User quits the puzzle
                elif event.key == K_RETURN:
                    if user_grid == solution:
                        return True  # Puzzle solved
                elif event.key == K_h:
                    # Provide a hint using Zelta
                    for row in range(9):
                        for col in range(9):
                            if user_grid[row][col] == 0:
                                user_grid[row][col] = solution[row][col]
                                break
                        else:
                            continue
                        break
                elif event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                    # Navigate between cells
                    if event.key == K_UP and selected_cell[0] > 0:
                        selected_cell[0] -= 1
                    elif event.key == K_DOWN and selected_cell[0] < 8:
                        selected_cell[0] += 1
                    elif event.key == K_LEFT and selected_cell[1] > 0:
                        selected_cell[1] -= 1
                    elif event.key == K_RIGHT and selected_cell[1] < 8:
                        selected_cell[1] += 1
                elif event.unicode.isdigit() and event.unicode != "0":
                    # Enter a number in the selected cell
                    row, col = selected_cell
                    if puzzle[row][col] == 0:  # Allow edits only on empty cells
                        user_grid[row][col] = int(event.unicode)

def game_loop():
    """Main game loop with story exploration and Sudoku."""
    current_node = 'day1_start'

    while True:
        screen.fill(WHITE)
        if current_node == 'day1_start':
            render_text(INTRO, 20)
            render_text(DAY_1, 100)
        else:
            prompt = prompt_graph.get_prompt(current_node)
            render_text(prompt, 20)

        if current_node == 'day1_sudoku':
            # Trigger Sudoku puzzle
            render_text("Solve the Sudoku puzzle to progress...", 300)
            pygame.display.flip()

            if sudoku_puzzle():
                render_text("Congratulations! You've unlocked the next step!", 400, color=GREEN)
                pygame.display.flip()
                pygame.time.wait(3000)
                current_node = 'end_game'
            else:
                render_text("Failed to solve the puzzle. Try again!", 400, color=RED)
                pygame.display.flip()
                pygame.time.wait(3000)
                break

        # Display options for next steps
        next_nodes = prompt_graph.get_next_nodes(current_node)
        render_choices([prompt_graph.get_prompt(node) for node in next_nodes] + ["Quit Game"], 400)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key in [K_1, K_2, K_3]:
                    idx = event.key - K_1
                    if idx < len(next_nodes):
                        current_node = next_nodes[idx]
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()

        if current_node == 'end_game':
            screen.fill(WHITE)
            render_text("Game Won! You woke up and discovered it was a dream.", 200, color=GREEN)
            pygame.display.flip()
            pygame.time.wait(5000)
            break

game_loop()