from ftcc.compilation_layers.qiskit_layer import QiskitBicycleLayer


def test_bicycle_simple():
    circuit = """{"Rotation":{"basis":["X","X","I","I","I","I","I","I","I","I","I","Y"],"angle":"0.125"}}
    {"Rotation":{"basis":["Z","Z","I","I","I","I","I","I","I","I","I","I"],"angle":"0.5"}}
    {"Rotation":{"basis":["X","X","I","I","I","I","I","I","I","I","I","I"],"angle":"-0.125"}}
    {"Measurement":{"basis":["Z","X","I","I","I","I","I","I","I","I","I","I"],"flip_result":true}}
    {"Measurement":{"basis":["X","I","I","I","I","Z","I","I","I","I","I","I"],"flip_result":false}}
    """
    metadata = {
        "code_name": "gross",
        "code_n": 144,
        "code_k": 12,
        "code_d": 12,
    }

    bicycle_layer = QiskitBicycleLayer(circuit, metadata)
    bicycle_layer.compile()
    print(bicycle_layer.circuit)

    return
