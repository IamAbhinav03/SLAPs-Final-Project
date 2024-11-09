import networkx as nx

class PromptGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id, prompt):
        self.graph.add_node(node_id, prompt=prompt)

    def add_edge(self, from_node, to_node):
        self.graph.add_edge(from_node, to_node)

    def get_prompt(self, node_id):
        return self.graph.nodes[node_id]['prompt']
    
    def get_next_nodes(self, node_id):
        return list(self.graph.successors(node_id))
