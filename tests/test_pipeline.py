import pytest
from qiskit import QuantumCircuit as QiskitCircuit
from qiskit.circuit.random import random_clifford_circuit
import qiskit.qasm2 as qasm2
import pyzx as zx

from ftcc.compilation_layers import (
    QiskitPBCLayer,
    QiskitBicycleLayer,
    MQTEncodingLayer,
    TopologiqLayer,
    TQECLayer,
    PyZXLayer,
)
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


def test_pipeline_ls():
    qc = QiskitCircuit(10)
    qc.h(0)
    qc.cx(0, 3)
    qc.cx(0, 4)
    qc.cx(0, 5)
    qc.cx(0, 6)
    qc.h(0)
    qc.h(1)
    qc.cx(1, 3)
    qc.cx(1, 4)
    qc.cx(1, 7)
    qc.cx(1, 8)
    qc.h(1)
    qc.h(2)
    qc.cx(2, 3)
    qc.cx(2, 5)
    qc.cx(2, 7)
    qc.cx(2, 9)
    qc.h(2)

    code_params = {
        "n": 7,
        "k": 1,
        "d": 3,
        "name": "Steane",
    }

    qasm_str = qasm2.dumps(qc)
    zx_circuit = zx.Circuit.from_qasm(qasm_str)

    pipeline = Pipeline(zx_circuit)
    compilation_path = [PyZXLayer, TopologiqLayer, TQECLayer]

    compiled_circuit = pipeline.compile(compilation_path, code_params)
    print(compiled_circuit)
    return


def test_pipeline_compile_args():
    qc = QiskitCircuit(10)
    qc.h(0)
    qc.cx(0, 3)
    qc.cx(0, 4)
    qc.cx(0, 5)
    qc.cx(0, 6)
    qc.h(0)
    qc.h(1)
    qc.cx(1, 3)
    qc.cx(1, 4)
    qc.cx(1, 7)
    qc.cx(1, 8)
    qc.h(1)
    qc.h(2)
    qc.cx(2, 3)
    qc.cx(2, 5)
    qc.cx(2, 7)
    qc.cx(2, 9)
    qc.h(2)

    code_params = {
        "n": 7,
        "k": 1,
        "d": 3,
        "name": "Steane",
    }

    qasm_str = qasm2.dumps(qc)
    zx_circuit = zx.Circuit.from_qasm(qasm_str)

    pipeline = Pipeline(zx_circuit)
    compilation_path = [PyZXLayer, TopologiqLayer, TQECLayer]
    args_dict = {
        TopologiqLayer: {"max_attempts": 1},
    }

    compiled_circuit = pipeline.compile(compilation_path, code_params, args_dict)
    print(compiled_circuit)
    return


@pytest.mark.parametrize("N", [3])
def test_mandatory_compile_args(N: int):
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
    args_dict = {
        QiskitPBCLayer: {"fix_clifford": True},
    }

    # run pipeline
    _ = pipeline.compile(compilation_path=compilation_path, compile_args=args_dict)

    # print(compiled_circuit)
    return


def test_pathfinding():
    qc = QiskitCircuit(10)
    qc.h(0)
    qc.cx(0, 3)
    qc.cx(0, 4)
    qc.cx(0, 5)
    qc.cx(0, 6)
    qc.h(0)
    qc.h(1)
    qc.cx(1, 3)
    qc.cx(1, 4)
    qc.cx(1, 7)
    qc.cx(1, 8)
    qc.h(1)
    qc.h(2)
    qc.cx(2, 3)
    qc.cx(2, 5)
    qc.cx(2, 7)
    qc.cx(2, 9)
    qc.h(2)

    code_params = {
        "n": 7,
        "k": 1,
        "d": 3,
        "name": "Steane",
    }

    qasm_str = qasm2.dumps(qc)
    zx_circuit = zx.Circuit.from_qasm(qasm_str)

    pipeline = Pipeline(zx_circuit)
    compilation_path = [PyZXLayer, TQECLayer]

    # This should do pathfinding to find TopologiqLayer connecting PyZXLayer with TQECLayer.
    _ = pipeline.compile(compilation_path=compilation_path, code_params=code_params)

    return
