import pyzx as zx
from topologiq.utils.interop_pyzx import pyzx_g_to_simple_g
from ftcc.compilation_layers.topologiq_layer import TopologiqLayer
from qiskit import qasm2


def translate_mqt_encoding_to_topologiq(mqt_encoding_layer):
    """
    Creates a TopologiqLayer object from a compiled PyZXLayer object.
    """

    mqt_circuit = mqt_encoding_layer.circuit
    qasm_circuit = qasm2.dumps(mqt_circuit)
    zx_circuit = zx.Circuit.from_qasm(qasm_circuit)
    zx_graph = zx_circuit.to_graph(zx_circuit)
    effect = "0" * mqt_encoding_layer.metadata["num_ancilla"] + "/" * (
        mqt_encoding_layer.metadata["num_qubits"]
        - mqt_encoding_layer.metadata["num_ancilla"]
    )
    zx_graph.apply_effect(effect)
    zx_graph.apply_state("0" * mqt_encoding_layer.metadata["num_qubits"])

    simple_graph = pyzx_g_to_simple_g(zx_graph)
    topologiq_layer = TopologiqLayer(simple_graph, metadata=mqt_encoding_layer.metadata)

    return topologiq_layer
