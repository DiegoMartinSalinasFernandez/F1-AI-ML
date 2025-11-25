import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------
#  ERROR SYSTEM
# ---------------------------------------------------------
errors = [
    ("SYS", 0)
]


# ---------------------------------------------------------
#  TRACK STRUCTURE (FUTURE USE)
# ---------------------------------------------------------
class Track:
    """
    This class will later contain information such as:
    - number of corners,
    - number of straights,
    - maximum length,
    - elevation,
    - sector distribution.

    For now it acts mainly as a placeholder.
    """
    def __init__(self, curvas: int, rectas: int, max_large: float):
        self.curvas = curvas
        self.rectas = rectas
        self.max_large = max_large


# ---------------------------------------------------------
#  VERTEX OBJECT
# ---------------------------------------------------------
class Vertex:
    def __init__(self, vertex_id):
        self.id = vertex_id


# ---------------------------------------------------------
#  GRAPH CLASS
# ---------------------------------------------------------
class Graph:
    def __init__(self):
        self.name = "Graph"

        self.vertices = {}

        self.adjacency_list = {}

        # Matrix and mapping
        self.adjacency_matrix = np.array([])
        self.id_to_index = {}
        self.index_counter = 0

    # -----------------------------------------------------
    #  ADD VERTEX
    # -----------------------------------------------------
    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:

        
            self.vertices[vertex_id] = Vertex(vertex_id)
            self.adjacency_list[vertex_id] = []

            
            new_index = self.index_counter
            self.id_to_index[vertex_id] = new_index
            self.index_counter += 1

           
            size = len(self.vertices)
            new_matrix = np.zeros((size, size))

            if self.adjacency_matrix.size > 0:
                old_size = self.adjacency_matrix.shape[0]
                new_matrix[:old_size, :old_size] = self.adjacency_matrix

            self.adjacency_matrix = new_matrix

    # -----------------------------------------------------
    #  REMOVE VERTEX
    # -----------------------------------------------------
    def remove_vertex(self, vertex_id):
        """
        Fully removes a vertex: list, matrix, and mapping.
        """
        if vertex_id not in self.vertices:
            raise NameError(f"{errors[0][0]} | {self.name} | That vertex doesn't exist.")

        index_to_remove = self.id_to_index[vertex_id]

        self.vertices.pop(vertex_id)
        self.adjacency_list.pop(vertex_id)

        for src in self.adjacency_list:
            self.adjacency_list[src] = [
                (dst, w) for (dst, w) in self.adjacency_list[src]
                if dst != vertex_id
            ]

        self.adjacency_matrix = np.delete(self.adjacency_matrix, index_to_remove, axis=0)
        self.adjacency_matrix = np.delete(self.adjacency_matrix, index_to_remove, axis=1)

        self.id_to_index.pop(vertex_id)
        new_mapping = {}
        for i, key in enumerate(self.id_to_index.keys()):
            new_mapping[key] = i
        self.id_to_index = new_mapping

    # -----------------------------------------------------
    #  ADD EDGE (UNDIRECTED BY DEFAULT)
    # -----------------------------------------------------
    def add_edge(self, src_id, dest_id, weight=1, undirected=True):

        if src_id not in self.vertices:
            self.add_vertex(src_id)
        if dest_id not in self.vertices:
            self.add_vertex(dest_id)

        self.adjacency_list[src_id].append((dest_id, weight))

        if undirected:
            self.adjacency_list[dest_id].append((src_id, weight))

        src_index = self.id_to_index[src_id]
        dest_index = self.id_to_index[dest_id]

        self.adjacency_matrix[src_index, dest_index] = weight

        if undirected:
            self.adjacency_matrix[dest_index, src_index] = weight

    # -----------------------------------------------------
    #  GET ADJ MATRIX
    # -----------------------------------------------------
    def get_adjacency_matrix(self):
        return self.adjacency_matrix, self.id_to_index

    # -----------------------------------------------------
    #  GRAPH VISUALIZATION (NETWORKX)
    # -----------------------------------------------------
    def visualize_graph(self):
        """
        Uses NetworkX to draw the graph.
        Now supports undirected visualization.
        """
        G = nx.Graph()  

        for vertex_id in self.vertices:
            G.add_node(vertex_id)

        for src, edges in self.adjacency_list.items():
            for dest, weight in edges:
                G.add_edge(src, dest, weight=weight)

        pos = nx.spring_layout(G, seed=4)

        nx.draw_networkx_nodes(G, pos, node_size=1200, node_color="skyblue", linewidths=2)
        nx.draw_networkx_edges(G, pos, width=2, edge_color="gray")
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Track Graph (Undirected)")
        plt.axis("off")
        plt.show()
