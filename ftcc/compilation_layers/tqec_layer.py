import tqec
from tqec.utils.enums import Basis

class TQECLayer(base_layer.BaseLayer):
    """
    aa
    """

    def __init__(self, filled_block_graph):
        """
        aa
        """

        self.filled_block_graph = filled_block_graph


    def compile(self, observable_basis):
        """
        aa
        """

        block_graph_for_computation = graphs_for_given_basis(self.filled_block_graph, observable_basis)
        compiled_graph = compile_block_graph(block_graph_for_computation)
        stim_circuit = compiled_graph.generate_stim_circuit(
            k=self.metadata["code_k"], noise_model=None
        )
        self.stim_circuit = stim_circuit
        self.metadata["tqec_correlation_surfaces"] = block_graph_for_computation.find_correlation_surfaces()

        return


    def graphs_for_given_basis(pre_filled_block_graphs, observable_basis: Basis) -> BlockGraph | None:

        filled_graphs = pre_filled_block_graphs
        assert len(filled_graphs) == 2
        if observable_basis == Basis.X:
            return filled_graphs[0].graph
        elif observable_basis == Basis.Z:
            return filled_graphs[1].graph



