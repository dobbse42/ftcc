import networkx as nx
from matplotlib import pyplot as plt

from typing import Optional

from ftcc.compilation_layers import (
    QiskitPBCLayer,
    QiskitBicycleLayer,
    PyZXLayer,
    TQECLayer,
    TopologiqLayer,
    MQTEncodingLayer,
    NWQECTranspilationLayer,
    NWQECPauliLayer,
)


class CompilationGraph:
    def __init__(
        self,
        excluded_nodes: Optional[str] = None,
        excluded_edges: Optional[tuple[str, str]] = None,
    ):
        """
        Creates a compilation graph with potentially excluded nodes and edges
        """
        self.graph = self.create_graph(
            excluded_nodes=excluded_nodes, excluded_edges=excluded_edges
        )

    def create_graph(
        self,
        excluded_nodes: str,
        excluded_edges: str,
    ) -> nx.Graph():
        """
        Creates a compilation graph of all known layers and translation layers except those specifed as excluded.
        """
        graph = nx.DiGraph()

        graph.add_node(PyZXLayer)
        graph.add_node(MQTEncodingLayer)
        graph.add_node(TopologiqLayer)
        graph.add_node(TQECLayer)
        # graph.add_node("lsqeccLayer")
        # graph.add_node("TISCCLayer")
        graph.add_node(QiskitPBCLayer)
        graph.add_node(QiskitBicycleLayer)
        graph.add_node(NWQECTranspilationLayer)
        graph.add_node(NWQECPauliLayer)

        graph.add_edge(MQTEncodingLayer, PyZXLayer)
        graph.add_edge(PyZXLayer, TopologiqLayer)
        graph.add_edge(TopologiqLayer, TQECLayer)
        # graph.add_edge("lsqecc", "TISCC")
        graph.add_edge(QiskitPBCLayer, QiskitBicycleLayer)
        graph.add_edge(NWQECTranspilationLayer, NWQECPauliLayer)
        graph.add_edge(NWQECPauliLayer, QiskitBicycleLayer)

        return graph

    def display_graph(self):
        """
        Basic drawing of the compilation graph using matplotlib. Assumes user can dispaly svgs.
        """
        # ax = plt.subplot(121) # I don't remember why this was necessary
        nx.draw(self.graph, with_labels=True)
        plt.show()
        # plt.savefig("compilation-graph.svg")
        return
