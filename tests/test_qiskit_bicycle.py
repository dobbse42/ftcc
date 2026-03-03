import pytest
from qiskit import QuantumCircuit as QiskitCircuit

# from qiskit.quantum_info import Operator, SparseObservable, Pauli
# from qiskit.circuit.library import PauliProductMeasurement, PauliEvolutionGate
from qiskit.circuit.random import random_clifford_circuit

from ftcc.compilation_layers.qiskit_layer import QiskitBicycleLayer, QiskitPBCLayer
from ftcc.translation_layers.qiskit_pbc_to_bicycle import (
    translate_qiskit_pbc_to_bicycle,
)


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


@pytest.mark.parametrize("N", [3, 5, 7])
def test_qiskit_pbc_bicycle_translation(N: int):
    qc = QiskitCircuit(N)
    for layer in range(N):
        clifford_circuit = random_clifford_circuit(
            num_qubits=N, num_gates=N**2, gates="all"
        )
        qc.compose(clifford_circuit, inplace=True)
        qc.t(0)
        qc.tdg(1)
    metadata = {
        "code_name": "gross",
        "code_n": 144,
        "code_k": 12,
        "code_d": 12,
    }

    pbc_layer = QiskitPBCLayer(qc, metadata)
    pbc_layer.compile(fix_clifford=False)
    bicycle_layer = translate_qiskit_pbc_to_bicycle(pbc_layer)
    bicycle_layer.compile()
    print(bicycle_layer.circuit)
