# from tqec.interop.collada.read_write import read_from_lattice_dicts
# from tqec.interop.pyzx.topologiq import read_from_lattice_dicts
from tqec.interop.bgraph.read_write import load_bgraph
from ftcc.compilation_layers import TopologiqLayer
from ftcc.compilation_layers import TQECLayer
from pathlib import Path


def translate_topologiq_to_tqec(topologiq_layer: TopologiqLayer):
    """
    Translates a circuit from the output of a topologiq layer to the input of a TQEC layer.
    """
    # lattice_edges = topologiq_layer.metadata["topologiq_lattice_edges"]
    # lattice_nodes = topologiq_layer.metadata["topologiq_lattice_nodes"]
    circuit_name = (
        topologiq_layer.metadata["NAME"]
        if "NAME" in topologiq_layer.metadata.keys()
        else "FT_circuit_placeholder_name"
    )

    # lattice_edges_min = dict([(k, v[0]) for k, v in lattice_edges.items()])
    # block_graph = read_from_lattice_dicts(
    #     lattice_nodes, lattice_edges_min, graph_name=circuit_name
    # )
    bgraph_manager = topologiq_layer.bgraph_manager

    bgraph_dir_name = "temp_topologiq_output_dir"
    bgraph_path = Path(bgraph_dir_name) / (circuit_name + ".bgraph")
    bgraph_manager.write_bgraph(output_dir=bgraph_dir_name, circuit_name=circuit_name)

    # tqec_bgraph = load_bgraph(bgraph_dir_name + "/" + circuit_name + ".bgraph")
    tqec_bgraph = load_bgraph(bgraph_path)

    # tqec_layer = TQECLayer(tqec_bgraph, topologiq_layer.metadata)

    filled_block_graphs = tqec_bgraph.fill_ports_for_minimal_simulation()
    tqec_layer = TQECLayer(filled_block_graphs, topologiq_layer.metadata)

    return tqec_layer
