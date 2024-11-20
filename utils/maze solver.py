import pygame
import random
import sys
from z3 import *

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 60
MAZE_ROWS = 5
MAZE_COLS = 5
NUM_MAZES = 2
SCREEN_WIDTH = CELL_SIZE * MAZE_COLS * NUM_MAZES + (NUM_MAZES - 1) * CELL_SIZE
SCREEN_HEIGHT = CELL_SIZE * MAZE_ROWS + 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class MazeGame:
    def __init__(self):
        self.mazes = []
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simultaneous Maze Solver")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        # Generate two different solvable mazes
        self.mazes = []
        self.player_positions = []
        
        for _ in range(NUM_MAZES):
            maze = self.generate_solvable_maze()
            self.mazes.append(maze)
            self.player_positions.append([0, 0])  # Start position
        
        self.moves = []
        self.game_won = False
        self.move_count = 0

    def generate_solvable_maze(self):
        maze = [[0] * MAZE_COLS for _ in range(MAZE_ROWS)]

        def is_path_exists(maze):
            start = (0, 0)
            goal = (MAZE_ROWS - 1, MAZE_COLS - 1)
            visited = set()
            queue = [start]

            while queue:
                current = queue.pop(0)
                if current == goal:
                    return True

                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    next_pos = (current[0] + dx, current[1] + dy)
                    if (0 <= next_pos[0] < MAZE_ROWS and
                        0 <= next_pos[1] < MAZE_COLS and
                        next_pos not in visited and
                        maze[next_pos[0]][next_pos[1]] == 0):
                        queue.append(next_pos)
                        visited.add(next_pos)
            return False

        while True:
            maze = [[random.choice([0, 0, 0, 1]) for _ in range(MAZE_COLS)] for _ in range(MAZE_ROWS)]
            maze[0][0] = 0
            maze[MAZE_ROWS - 1][MAZE_COLS - 1] = 0
            if is_path_exists(maze):
                return maze

    def generate_mazes(self):
        for _ in range(NUM_MAZES):
            self.mazes.append(self.generate_solvable_maze())

    def move_player(self, direction):
        if self.game_won:
            return

        self.moves.append(direction)
        self.move_count += 1
        
        # Update all maze positions
        for i in range(len(self.mazes)):
            new_pos = self.player_positions[i].copy()
            
            if direction == 'up' and new_pos[0] > 0:
                new_pos[0] -= 1
            elif direction == 'down' and new_pos[0] < MAZE_ROWS - 1:
                new_pos[0] += 1
            elif direction == 'left' and new_pos[1] > 0:
                new_pos[1] -= 1
            elif direction == 'right' and new_pos[1] < MAZE_COLS - 1:
                new_pos[1] += 1
                
            # Check if move is valid (no obstacle)
            if self.mazes[i][new_pos[0]][new_pos[1]] == 0:
                self.player_positions[i] = new_pos

        # Check if all mazes are solved
        self.check_win()

    def check_win(self):
        for pos in self.player_positions:
            if pos != [MAZE_ROWS-1, MAZE_COLS-1]:
                return
        self.game_won = True

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw each maze
        for maze_idx, maze in enumerate(self.mazes):
            offset_x = maze_idx * (MAZE_COLS * CELL_SIZE + CELL_SIZE)
            
            # Draw maze cells
            for row in range(MAZE_ROWS):
                for col in range(MAZE_COLS):
                    x = offset_x + col * CELL_SIZE
                    y = row * CELL_SIZE
                    
                    # Draw cell
                    pygame.draw.rect(self.screen, BLACK if maze[row][col] else WHITE,
                                   (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK,
                                   (x, y, CELL_SIZE, CELL_SIZE), 1)
            
            # Draw player
            player_x = offset_x + self.player_positions[maze_idx][1] * CELL_SIZE
            player_y = self.player_positions[maze_idx][0] * CELL_SIZE
            pygame.draw.circle(self.screen, RED,
                             (player_x + CELL_SIZE//2, player_y + CELL_SIZE//2),
                             CELL_SIZE//3)
            
            # Draw goal
            goal_x = offset_x + (MAZE_COLS-1) * CELL_SIZE
            goal_y = (MAZE_ROWS-1) * CELL_SIZE
            pygame.draw.rect(self.screen, GREEN,
                           (goal_x + CELL_SIZE//4, goal_y + CELL_SIZE//4,
                            CELL_SIZE//2, CELL_SIZE//2))

        # Draw move count
        moves_text = self.font.render(f"Moves: {self.move_count}", True, BLACK)
        self.screen.blit(moves_text, (10, SCREEN_HEIGHT - 50))

        # Draw win message
        if self.game_won:
            win_text = self.font.render("You Won!", True, BLUE)
            self.screen.blit(win_text, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT - 50))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif not self.game_won:
                        if event.key == pygame.K_UP:
                            self.move_player('up')
                        elif event.key == pygame.K_DOWN:
                            self.move_player('down')
                        elif event.key == pygame.K_LEFT:
                            self.move_player('left')
                        elif event.key == pygame.K_RIGHT:
                            self.move_player('right')
            
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def solve_mazes_with_z3(self):
        # Z3 variables
        max_steps = MAZE_ROWS * MAZE_COLS
        x = [[Int(f"x{i}_{t}") for t in range(max_steps)] for i in range(NUM_MAZES)]
        y = [[Int(f"y{i}_{t}") for t in range(max_steps)] for i in range(NUM_MAZES)]
        solver = Solver()

        directions = ["up", "down", "left", "right"]
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Constraints for all mazes
        for i in range(NUM_MAZES):
            maze = self.mazes[i]

            # Start and goal positions
            solver.add(x[i][0] == 0, y[i][0] == 0)  # Start
            solver.add(x[i][max_steps - 1] == MAZE_ROWS - 1, y[i][max_steps - 1] == MAZE_COLS - 1)  # End

            for t in range(max_steps):
                # Within bounds
                solver.add(And(0 <= x[i][t], x[i][t] < MAZE_ROWS))
                solver.add(And(0 <= y[i][t], y[i][t] < MAZE_COLS))

                # Avoid obstacles
                for r in range(MAZE_ROWS):
                    for c in range(MAZE_COLS):
                        if maze[r][c] == 1:  # Obstacle
                            solver.add(Not(And(x[i][t] == r, y[i][t] == c)))

                # Valid moves
                if t < max_steps - 1:
                    move_constraints = []
                    for dir_idx, (dx, dy) in enumerate(moves):
                        move_constraints.append(
                            And(x[i][t + 1] == x[i][t] + dx, y[i][t + 1] == y[i][t] + dy)
                        )
                    solver.add(Or(move_constraints))

        # Solve for shortest path
        if solver.check() == sat:
            model = solver.model()
            shortest_path = []
            for i in range(max_steps - 1):
                x0, y0 = model[x[0][i]].as_long(), model[y[0][i]].as_long()
                x1, y1 = model[x[0][i + 1]].as_long(), model[y[0][i + 1]].as_long()
                for dir_idx, (dx, dy) in enumerate(moves):
                    if x1 == x0 + dx and y1 == y0 + dy:
                        shortest_path.append(directions[dir_idx])
                        break
            return shortest_path

        return []

if __name__ == "__main__":
    game = MazeGame()
    print("hello")
    shortest_moves = game.solve_mazes_with_z3()
    print("Shortest Moves to Solve Both Mazes:")
    print(shortest_moves)
    game.run()