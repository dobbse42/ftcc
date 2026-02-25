import pytest

import numpy as np
from ftcc.compilation_layers.qiskit_layer import QiskitPBCLayer

# from ftcc.translation_layers.mqt_to_qiskit_pbc import translate_mqt_to_qiskit_pbc
from qiskit import QuantumCircuit as QiskitCircuit
from qiskit.quantum_info import Operator, SparseObservable, Pauli
from qiskit.transpiler.passes import LitinskiTransformation
from qiskit.circuit.library import PauliProductMeasurement, PauliEvolutionGate
from qiskit.circuit.random import random_clifford_circuit


def test_qiskit_pbc_t():
    """
    Adapted from test_litinski_transformation.py in Qiskit 2.3
    """
    metadata = {}

    qc = QiskitCircuit(4)
    qc.h(0)
    qc.cx(0, 1)
    qc.t(0)
    qc.cx(0, 2)
    qc.t(1)
    qc.tdg(0)
    qc.s(2)
    qc.t(2)

    qiskit_layer = QiskitPBCLayer(qc, metadata)

    qiskit_layer.compile()
    # qct = LitinskiTransformation(fix_clifford=True)(qc)
    qct = qiskit_layer.circuit
    assert qct.count_ops() == {"PauliEvolution": 4, "cx": 2, "h": 1, "s": 1}
    assert Operator(qct) == Operator(qc)

    return


@pytest.mark.parametrize("N", [5, 7, 9])
def test_qiskit_pbc_random(N: int):
    """
    Adapted from test_random_circuits in Qiskit's test_litisnki_transformation.py
    """
    qc = QiskitCircuit(N)
    for layer in range(N):
        clifford_circuit = random_clifford_circuit(
            num_qubits=N, num_gates=N**2, gates="all"
        )
        qc.compose(clifford_circuit, inplace=True)
        qc.t(0)
        qc.tdg(1)

    metadata = {}
    qiskit_layer = QiskitPBCLayer(qc, metadata)
    qiskit_layer.compile()

    qct = qiskit_layer.circuit
    assert "T" not in qct.count_ops()
    assert "tdg" not in qct.count_ops()

    assert Operator(qct) == Operator(qc)

    return


def test_qiskit_pbc_measure():
    """
    Adapted from test_on_circuits_with_measures() in Qiskit's test_litinski_transformation.py
    """
    # This is the example from Figure 4 in the paper "A Game of Surface Codes" by Litinski.

    # The original circuit (as shown at the top-left of the figure).
    qc = QiskitCircuit(4, 4)
    qc.t(0)
    qc.cx(2, 1)
    qc.sxdg(3)
    qc.cx(1, 0)
    qc.sx(2)
    qc.t(3)
    qc.cx(3, 0)
    qc.t(0)
    qc.s(1)
    qc.t(2)
    qc.s(3)
    qc.sxdg(0)
    qc.sx(1)
    qc.sx(2)
    qc.sx(3)
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.measure(2, 2)
    qc.measure(3, 3)
    # Apply the Litinski transform with fix_cliffords=False (ignoring the Clifford gates
    # at the end of the transformed circuit, and clearing the global phase).
    metadata = {}
    qiskit_layer = QiskitPBCLayer(qc, metadata)
    qiskit_layer.compile(fix_clifford=False)
    qct = qiskit_layer.circuit
    qct.global_phase = 0

    # The transformed circuit (as shown at the bottom-right of the figure).
    expected = QiskitCircuit(4, 4)
    expected.append(
        PauliEvolutionGate(SparseObservable.from_list([("Z", 1)]), np.pi / 8), [0]
    )
    expected.append(
        PauliEvolutionGate(SparseObservable.from_list([("YX", 1)]), np.pi / 8), [1, 2]
    )
    expected.append(
        PauliEvolutionGate(SparseObservable.from_list([("Y", 1)]), -np.pi / 8), [3]
    )
    expected.append(
        PauliEvolutionGate(SparseObservable.from_list([("YZZZ", 1)]), -np.pi / 8),
        [0, 1, 2, 3],
    )
    expected.append(PauliProductMeasurement(Pauli("YZZY")), [0, 1, 2, 3], [0])
    expected.append(PauliProductMeasurement(Pauli("XX")), [0, 1], [1])
    expected.append(PauliProductMeasurement(Pauli("-Z")), [2], [2])
    expected.append(PauliProductMeasurement(Pauli("XX")), [0, 3], [3])

    assert qct == expected
