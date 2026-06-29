# from topologiq.input.pyzx import pyzx_g_to_simple_g
from ftcc.compilation_layers import TopologiqLayer


def translate_pyzx_to_topologiq(pyzx_layer):
    """
    Creates a TopologiqLayer object from a compiled PyZXLayer object.
    """

    # pyzx_layer.graph.apply_state("0" * pyzx_layer.metadata["num_qubits"])
    """pyzx_layer.graph.apply_effect(
        "0" * pyzx_layer.metadata["num_ancilla"]
        + "/" * (pyzx_layer.metadata["num_qubits"] - pyzx_layer.metadata["num_ancilla"])
    )"""
    # pyzx_layer.compile(apply_state=True, apply_effect=True)

    # simple_graph = pyzx_g_to_simple_g(pyzx_layer.graph)
    # print(simple_graph)
    # topologiq_layer = TopologiqLayer(simple_graph, metadata=pyzx_layer.metadata)
    topologiq_layer = TopologiqLayer(pyzx_layer.graph, metadata=pyzx_layer.metadata)

    return topologiq_layer
