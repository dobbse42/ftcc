import pytest
from qiskit import QuantumCircuit as QiskitCircuit
from qiskit.circuit.random import random_circuit
from qiskit import qasm2
import tempfile
import nwqec

from ftcc.compilation_layers import (
    NWQECTranspilationLayer,
    NWQECPauliLayer,
    QiskitBicycleLayer,
)
from ftcc.translation_layers.nwqec_transpilation_to_pauli import (
    translate_nwqec_transpilation_to_pauli,
)
from ftcc import Pipeline


pytestmark = pytest.mark.build


def generate_random_nwqec_circuit(N: int):
    qiskit_circuit = random_circuit(
        N, N**2, measure=False, conditional=False, reset=False, seed=42
    )

    # Remove excluded gates
    excluded_gates = {"ecr", "c3sx", "id"}
    to_remove = []
    for i, gate in enumerate(qiskit_circuit.data):
        # print(f"gate {i} is {gate.name}")
        if gate.name in excluded_gates:
            # print(f"found excluded gate {gate.name}")
            to_remove.append(i)
    num_removed = 0
    for idx in to_remove:
        del qiskit_circuit.data[idx - num_removed]
        num_removed += 1
    # Make nwqec circuit
    with tempfile.NamedTemporaryFile() as tmp:
        qasm2.dump(qiskit_circuit, tmp.name)
        nwqec_circuit = nwqec.load_qasm(tmp.name)

    return nwqec_circuit


@pytest.mark.parametrize("N", [5, 7, 9])
def test_nwqec_end_to_end(N: int):
    nwqec_circuit = generate_random_nwqec_circuit(N)

    pipeline = Pipeline(nwqec_circuit)
    compilation_path = [NWQECTranspilationLayer, NWQECPauliLayer, QiskitBicycleLayer]

    pipeline.compile(compilation_path)


@pytest.mark.parametrize("N", [3, 5, 7])
def test_nwqec_translation(N: int):
    nwqec_circuit = generate_random_nwqec_circuit(N)
    metadata = {}

    transpilation_layer = NWQECTranspilationLayer(nwqec_circuit, metadata)
    transpilation_layer.compile()

    pbc_layer = translate_nwqec_transpilation_to_pauli(transpilation_layer)
    pbc_layer.compile()

    print(pbc_layer.circuit.count_ops())

    return
