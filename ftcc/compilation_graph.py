import networkx as nx
from matplotlib import pyplot as plt

class CompilationGraph:


    def __init__(
        self,
        excluded_nodes: Optional[str] = None,
        excluded_edges: Optional[tuple[str, str]] = None,
    ):
        """
        Creates a compilation graph with potentially excluded nodes and edges?
        """
        self.graph = self.create_graph(excluded_nodes=excluded_nodes, excluded_edges=excluded_edges)

    def create_graph(
        self,
        excluded_nodes: str,
        excluded_edges: str,
    ): -> nx.Graph
        """
        Creates a compilation graph of all known layers and translation layers except those specifed as excluded.
        """
        graph = nx.Graph()
        
        graph.add_node("PyZX")
        graph.add_node("MQT")
        graph.add_node("Qualtran")
        graph.add_node("Topologiq")
        graph.add_node("TQEC")
        graph.add_node("lsqecc")
        graph.add_node("TISCC")
        graph.add_node("Cirq")

        graph.add_edge(("MQT", "PyZX"))
        graph.add_edge(("Qualtran", "PyZX"))
        graph.add_edge(("Qualtran", "Cirq"))
        graph.add_edge(("PyZX", "Topologiq"))
        graph.add_edge(("Topologiq", "TQEC"))
        graph.add_edge(("lsqecc", "TISCC"))

        return graph


    def display_graph(self):
        """
        Basic drawing of the compilation graph using matplotlib. Assumes user can dispaly svgs.
        """
        ax = plt.subplot(121)
        nx.draw(self.graph, with_labels=True)
        plt.show()
        return
