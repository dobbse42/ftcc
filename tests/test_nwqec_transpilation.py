import pytest
import nwqec

from qiskit.circuit.random import random_circuit
from qiskit import qasm2
import tempfile

from ftcc.compilation_layers.nwqec_layer import NWQECTranspilationLayer


pytestsmark = pytest.mark.build


@pytest.mark.parametrize("N", [3, 5, 7, 9, 11])
def test_cliffordt(N: int):
    """
    Rationale for excluded gates:
    - ecr: While ECR gates have a type in NWQEC, they are not handled in the Clifford+T transpilation.
    - id: Identity gates are not included in the list of Clifford gates in NWQEC
    - c3sx: Controlled 3-qubit sqrt-X gates are not known to the NWQEC parser

    Only circuits excluded these three types of gates are tested.
    """
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

    # Compile
    metadata = {}
    nwqec_layer = NWQECTranspilationLayer(nwqec_circuit, metadata)
    print(nwqec_layer.circuit.count_ops())

    nwqec_layer.compile()
    # print(nwqec_layer.circuit.count_ops())
    assert nwqec_layer.circuit.is_clifford_t()

    return
