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

    @classmethod
    def set_compile_args(cls, flags, compile_args):
        """
        List of all possible compile_args:
        compile_args = {
            "weights": None,
            "first_id_strategy": None,
            "beams_len_short": None,
            "seed": None,
            "vis_options": None,
            "max_attempts": None,
            "stop_on_first_success": None,
            "min_succ_rate": None,
            "strip_ports": None,
            "hide_ports": None,
            "log_stats": None,
            "log_stats_id": None,
            "debug": None,
        }"""
        # compile_args = {"max_attempts": 5}
        if flags["use_fixed_seed"]:
            compile_args["seed"] = flags["fixed_seed_value"]

        return compile_args

    @classmethod
    def compilation_flags(cls):
        compilation_flags = {}
        return compilation_flags

    def compile(self):
        """
        Com
        """
        circuit_name = (
            self.metadata["NAME"]
            if "name" in self.metadata.keys()
            else "FT_circuit_name_placeholder"
        )

        kwargs = self.compile_args

        simple_graph_after_use, edge_paths, lattice_nodes, lattice_edges = runner(
            self.circuit,
            circuit_name,
            **kwargs,
        )

        if lattice_nodes is None or lattice_edges is None:
            raise RuntimeError(
                "Topologiq timed out. Try again with more attempts (set the more_attempts compile arg) if you think this circuit should work. However, it may be the case that topologiq simply cannot compile this circuit."
            )
        else:
            self.metadata["topologiq_edge_paths"] = edge_paths
            self.metadata["topologiq_lattice_nodes"] = lattice_nodes
            self.metadata["topologiq_lattice_edges"] = lattice_edges
            self.simple_graph = simple_graph_after_use

        return
