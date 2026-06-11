import networkx as nx
from matplotlib import pyplot as plt
from typing import Optional

import os
import ast
from pathlib import Path
# from ftcc.translation_registry import translation_dictionary

"""from ftcc.compilation_layers import (
    QiskitPBCLayer,
    QiskitBicycleLayer,
    PyZXLayer,
    TQECLayer,
    TopologiqLayer,
    MQTEncodingLayer,
    NWQECTranspilationLayer,
    NWQECPauliLayer,
    BaseLayer,
)"""


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

        graph.add_node(
            "BaseLayer"
        )  # this is a dummy node for testing purposes. It should never be used.
        graph.add_node("PyZXLayer")
        graph.add_node("MQTEncodingLayer")
        graph.add_node("TopologiqLayer")
        graph.add_node("TQECLayer")
        # graph.add_node("lsqeccLayer")
        # graph.add_node("TISCCLayer")
        graph.add_node("QiskitPBCLayer")
        graph.add_node("QiskitBicycleLayer")
        graph.add_node("NWQECTranspilationLayer")
        graph.add_node("NWQECPauliLayer")

        graph.add_edge("MQTEncodingLayer", "PyZXLayer")
        graph.add_edge("PyZXLayer", "TopologiqLayer")
        graph.add_edge("TopologiqLayer", "TQECLayer")
        # graph.add_edge("lsqecc", "TISCC")
        graph.add_edge("QiskitPBCLayer", "QiskitBicycleLayer")
        graph.add_edge("NWQECTranspilationLayer", "NWQECPauliLayer")
        graph.add_edge("NWQECPauliLayer", "QiskitBicycleLayer")

        return graph

    def display_graph(self):
        """
        Basic drawing of the compilation graph using matplotlib. Assumes user can display svgs.
        """
        # ax = plt.subplot(121) # I don't remember why this was necessary
        nx.draw(self.graph, with_labels=True)
        plt.show()
        # plt.savefig("compilation-graph.svg")
        return


"""    def get_requirements(self, compilation_path):
        translation_layers = []

        prev_node = compilation_path[0] # this is the source
        for node in compilation_path[1:]:
            translation_layers.append(translation_dictionary[(prev_node, node)])
            prev_node = node

        filenames = []
        for layer in compilation_path:
            module_name = layer.__module__
            filename = "src/ftcc/compilation_layers/" + module_name.split('.')[-1] + ".py"
            filenames.append(filename)

        for layer in translation_layers:
            module_names = layer.__module__
            filename = "src/ftcc/translation_layers/" + module_name.split('.')[-1] + ".py"
            filenames.append(filename)

        # Get list of imported modules
        modules = {}
        for filename in filenames:
            # this needs to be an update
            modules.update(self.get_external_modules(filename))

        return modules"""

"""    def get_external_modules(self, filename):
        source = Path(filename).read_text()
        tree = ast.parse(source, filename=filename)

        modules = {}
        for node in ask.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    modules.add(node.module.split('.')[0])

        external = sorted(
            m for m in modules
            if m not in sys.stdlib_module_names
        )

        return external"""
