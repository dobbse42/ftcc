import pytest
from qiskit import QuantumCircuit as QiskitCircuit
from qiskit.circuit.random import random_clifford_circuit

from ftcc.compilation_layers import QiskitPBCLayer, QiskitBicycleLayer
from ftcc import Pipeline


@pytest.mark.parametrize("N", [3, 4, 5])
def test_pipeline_compile(N: int):
    # create random test circuit
    qc = QiskitCircuit(N)
    for layer in range(N):
        clifford_circuit = random_clifford_circuit(
            num_qubits=N, num_gates=N**2, gates="all"
        )
        qc.compose(clifford_circuit, inplace=True)
        qc.t(0)
        qc.tdg(1)

    # create pipeline
    pipeline = Pipeline(qc)
    compilation_path = [QiskitPBCLayer, QiskitBicycleLayer]

    # run pipeline
    compiled_circuit = pipeline.compile(compilation_path=compilation_path)

    print(compiled_circuit)
    return
