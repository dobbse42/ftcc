from topologiq.scripts.runner import runner
from ftcc.compilation_layers.base_layer import BaseLayer


class TopologiqLayer(BaseLayer):
    """
    Adapted from Purva Thakre's end-to-end TQEC example notebook at:
    https://github.com/tqec/tqec/blob/e5d927e13ce8e20197134e42d082907c2d12151d/examples/notebooks/framework_integration.ipynb
    """

    def __init__(self, input_circ, metadata):
        """
        aa
        """

        self.circuit = input_circ
        self.metadata = metadata

    def compile(self):
        """
        Com
        """
        circuit_name = (
            self.metadata["NAME"]
            if "name" in self.metadata.keys()
            else "FT_circuit_name_placeholder"
        )
        visualization = None
        animation = None

        VALUE_FUNCTION_HYPERPARAMS = (
            -1,  # weight for length of path
            -1,  # weight for number of "beams" broken by path
        )

        kwargs = {
            "weights": VALUE_FUNCTION_HYPERPARAMS,
            "length_of_beams": 9,
        }

        simple_graph_after_use, edge_paths, lattice_nodes, lattice_edges = runner(
            self.circuit,
            circuit_name,
            visualize=(visualization, animation),
            **kwargs,
        )

        if lattice_nodes is None or lattice_edges is None:
            raise RuntimeError("topologiq failed")
        else:
            self.metadata["topologiq_edge_paths"] = edge_paths
            self.metadata["topologiq_lattice_nodes"] = lattice_nodes
            self.metadata["topologiq_lattice_edges"] = lattice_edges
            self.simple_graph = simple_graph_after_use

        return
