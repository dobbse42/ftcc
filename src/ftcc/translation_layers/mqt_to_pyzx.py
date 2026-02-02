import pyzx as zx
from ftcc.compilation_layers.pyzx_layer import PyZXLayer
from qiskit import qasm2


def translate_mqt_encoding_to_pyzx(mqt_encoding_layer):
    """
    Creates a PyZXLayer object from an MQTEncodingLayer object for a Steane code encoding circuit.
    """
    mqt_circuit = mqt_encoding_layer.circuit
    qasm_circuit = qasm2.dumps(mqt_circuit)
    zx_circuit = zx.Circuit.from_qasm(qasm_circuit)

    zx_graph = zx_circuit.to_graph(zx_circuit)
    num_apply_state = zx_graph.num_inputs()
    zx_graph.apply_state("0" * num_apply_state)
    zx_graph.apply_effect("///////")
    pyzx_layer = PyZXLayer(zx_graph, metadata=mqt_encoding_layer.metadata)

    return pyzx_layer
