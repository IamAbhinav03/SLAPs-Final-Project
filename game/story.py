
"""
Contains the game's story, including the intro, day descriptions, and ending scnearios.
"""

from .graph import PromptGraph

INTRO = """
Welcome to Logic Island Survival!

You are a skilled logician and programmer who has always been fascinated by the potential of artifical intelligence to solve complex problems. Your latest projecdt, a cutting-edge AI system designed to optimize resource allocation, has been gaining attention from various industries. However, just as you're about to showcase your system to potential investors, a sudden storm hits, and you're forced to evactuate to a nearby island.
"""

DAY_1 = """

Upon arrival, you realize that the island is unhabited, and your communication devices are damaged. With limited supplies, you must use your logical thinking to survive. You stumble upon an old, mysterious-looking computer in a abandoned reserach facility. As you boot it up, you discover a cryptic message:

Welcome, logician. Survive the island, and unlock the secrets of the optimal world. Solve the puzzles to progress.
"""

prompt_graph = PromptGraph()

# Add nodes and edges for Day 1
prompt_graph.add_node('day1_start', prompt="Welcome to Logic Island Survival...")
prompt_graph.add_node('day1_option1', prompt="Investigate the abandoned research facility...")
prompt_graph.add_node('day1_option2', prompt="Search the jungle for resources...")
prompt_graph.add_node('day1_option3', prompt="Follow the coastline to see if you can find any signs of civilization...")
prompt_graph.add_node('day1_option4', prompt="Use your logic skills to analyze your situation and come up with a plan...")
prompt_graph.add_node('day1_find_zeta', prompt="You find Zeta, your AI assistant...")
prompt_graph.add_node('day1_sudoku', prompt="Solve the Sudoku puzzle to unlock the next step...")

prompt_graph.add_edge('day1_start', 'day1_option1')
prompt_graph.add_edge('day1_start', 'day1_option2')
prompt_graph.add_edge('day1_start', 'day1_option3')

prompt_graph.add_edge('day1_option1', 'day1_find_zeta')
prompt_graph.add_edge('day1_option2', 'day1_find_zeta')
prompt_graph.add_edge('day1_option3', 'day1_find_zeta')

prompt_graph.add_edge('day1_find_zeta', 'day1_sudoku')

