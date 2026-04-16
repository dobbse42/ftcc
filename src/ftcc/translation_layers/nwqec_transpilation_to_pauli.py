from ftcc.compilation_layers.nwqec_layer import NWQECTranspilationLayer, NWQECPauliLayer


def translate_nwqec_transpilation_to_pauli(
    transpilation_layer: NWQECTranspilationLayer,
):
    metadata = transpilation_layer.metadata
    circuit = transpilation_layer.circuit

    return NWQECPauliLayer(circuit, metadata)
