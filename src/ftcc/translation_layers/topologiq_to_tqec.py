from tqec.interop.collada.read_write import read_from_lattice_dicts
from ftcc.compilation_layers.topologiq_layer import TopologiqLayer
from ftcc.compilation_layers.tqec_layer import TQECLayer


def translate_topologiq_to_tqec(topologiq_layer: TopologiqLayer):
    """
    Translates a circuit from the output of a topologiq layer to the input of a TQEC layer.
    """
    lattice_edges = topologiq_layer.metadata["topologiq_lattice_edges"]
    lattice_nodes = topologiq_layer.metadata["topologiq_lattice_nodes"]
    circuit_name = (
        topologiq_layer.metadata["NAME"]
        if "NAME" in topologiq_layer.metadata.keys()
        else "FT_circuit_placeholder_name"
    )

    lattice_edges_min = dict([(k, v[0]) for k, v in lattice_edges.items()])
    block_graph = read_from_lattice_dicts(
        lattice_nodes, lattice_edges_min, graph_name=circuit_name
    )
    filled_block_graphs = block_graph.fill_ports_for_minimal_simulation()
    tqec_layer = TQECLayer(filled_block_graphs, topologiq_layer.metadata)

    return tqec_layer
