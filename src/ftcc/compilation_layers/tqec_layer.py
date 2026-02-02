from ftcc.compilation_layers.base_layer import BaseLayer
from tqec.utils.enums import Basis
from tqec.computation.block_graph import BlockGraph
from tqec import compile_block_graph


class TQECLayer(BaseLayer):
    """
    aa
    """

    def __init__(self, filled_block_graph, metadata):
        """
        aa
        """

        self.metadata = metadata

        self.filled_block_graph = filled_block_graph

    def graphs_for_given_basis(
        self, pre_filled_block_graphs, observable_basis: Basis
    ) -> BlockGraph | None:
        filled_graphs = pre_filled_block_graphs
        # assert len(filled_graphs) == 2
        if observable_basis == Basis.X:
            return filled_graphs[0].graph
        elif observable_basis == Basis.Z:
            return filled_graphs[1].graph

    def compile(self, observable_basis):
        """
        aa
        """

        block_graph_for_computation = self.graphs_for_given_basis(
            self.filled_block_graph, observable_basis
        )
        compiled_graph = compile_block_graph(block_graph_for_computation)
        stim_circuit = compiled_graph.generate_stim_circuit(
            k=self.metadata["code_k"], noise_model=None
        )
        self.stim_circuit = stim_circuit
        self.metadata["tqec_correlation_surfaces"] = (
            block_graph_for_computation.find_correlation_surfaces()
        )

        return
