from.story import prompt_graph
from.story import INTRO
from.story import DAY_1
from.puzzles import sudoku_puzzle

def game_loop():
    print(INTRO)
    print(DAY_1)
    current_node = 'day1_start'

    while True:
        prompt = prompt_graph.get_prompt(current_node)
        print(prompt)

        if current_node == 'day1_sudoku':
            # Sudoku puzzle logic here
            print("Solve the Sudoku puzzle to unlock the next step...")
            if sudoku_puzzle():
                print("Congratulations, you've unlocked the next step!")
            else:
                print("Sorry, you didn't solve the puzzle correctly. Try again!")
            break

        next_nodes = prompt_graph.get_next_nodes(current_node)
        print("Choose a next step:")
        for i, node in enumerate(next_nodes):
            print(f"{i+1}. {prompt_graph.get_prompt(node)}")
        print(f"{len(next_nodes)+1}. Quit Game")

        choice = input("Enter your choice (1-{}): ".format(len(next_nodes)+1))
        print(len(next_nodes))
        if choice == str(len(next_nodes)+1):
            print("Thanks for playing! Goodbye.")
            break
        else:
            current_node = next_nodes[int(choice) - 1]

game_loop()