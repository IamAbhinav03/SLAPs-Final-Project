import curses

# Define a more complex maze structure
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
]

# Character's starting position
start_y, start_x = 1, 1
# Character's ending position
end_y, end_x = 7, 8

def draw_maze(stdscr, y, x):
    stdscr.clear()
    
    # Display the instructions and goal
    stdscr.addstr(0, 0, "Goal: Reach E")
    stdscr.addstr(1, 0, "Instructions:")
    stdscr.addstr(2, 0, "Use arrow keys to move")
    stdscr.addstr(3, 0, "Press 'q' to quit")

    for i, row in enumerate(MAZE):
        for j, cell in enumerate(row):
            if cell == 1:
                stdscr.addch(i + 4, j, '#')  # Wall (shifted down by 4)
            elif (i, j) == (start_y, start_x):
                stdscr.addch(i + 4, j, 'S')  # Start point (shifted down by 4)
            elif (i, j) == (end_y, end_x):
                stdscr.addch(i + 4, j, 'E')  # End point (shifted down by 4)
            else:
                stdscr.addch(i + 4, j, ' ')  # Path (shifted down by 4)
    
    stdscr.addch(y + 4, x, '@')  # Character (shifted down by 4)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    y, x = start_y, start_x
    draw_maze(stdscr, y, x)

    while True:
        key = stdscr.getch()

        # Move character based on key press
        if key == curses.KEY_UP and MAZE[y-1][x] == 0:
            y -= 1
        elif key == curses.KEY_DOWN and MAZE[y+1][x] == 0:
            y += 1
        elif key == curses.KEY_LEFT and MAZE[y][x-1] == 0:
            x -= 1
        elif key == curses.KEY_RIGHT and MAZE[y][x+1] == 0:
            x += 1
        elif key == ord('q'):  # Quit the game
            break

        draw_maze(stdscr, y, x)

        # Check if the player has reached the end point
        if (y, x) == (end_y, end_x):
            stdscr.addstr(0, 0, "You've reached the end! Press 'q' to quit.")
            stdscr.refresh()

curses.wrapper(main)