import pytest
import nwqec

from qiskit.circuit.random import random_circuit
from qiskit import qasm2
import tempfile

from ftcc.compilation_layers.nwqec_layer import NWQECTranspilationLayer


@pytest.mark.parametrize("N", [3, 5, 7, 9, 11])
def test_cliffordt(N: int):
    qiskit_circuit = random_circuit(
        N, N**2, measure=False, conditional=False, reset=False, seed=42
    )
    with tempfile.NamedTemporaryFile() as tmp:
        qasm2.dump(qiskit_circuit, tmp.name)
        nwqec_circuit = nwqec.load_qasm(tmp.name)

    metadata = {}
    nwqec_layer = NWQECTranspilationLayer(nwqec_circuit, metadata)
    print(nwqec_layer.circuit.count_ops())

    nwqec_layer.compile()
    # print(nwqec_layer.circuit.to_qasm_str())
    print(nwqec_layer.circuit.count_ops())
    assert nwqec_layer.circuit.is_clifford_t()

    return
