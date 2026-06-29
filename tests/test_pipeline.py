import pytest
import warnings
import pickle
from qiskit import QuantumCircuit as QiskitCircuit
from qiskit.circuit.random import random_clifford_circuit
import qiskit.qasm2 as qasm2
import pyzx as zx

from ftcc.compilation_layers import (
    QiskitPBCLayer,
    QiskitBicycleLayer,
    # MQTEncodingLayer,
    # TopologiqLayer,
    # TQECLayer,
    # PyZXLayer,
    BaseLayer,
)
from ftcc import Pipeline


pytestmark = pytest.mark.build


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
    compilation_path = ["QiskitPBCLayer", "QiskitBicycleLayer"]
    output_filename = "test_pipeline_compile.out"

    # run pipeline
    pipeline.compile(compilation_path=compilation_path, output_filename=output_filename)

    with open(output_filename, "rb") as f:
        compiled_circuit = pickle.load(f)
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
    compilation_path = ["PyZXLayer", "TopologiqLayer", "TQECLayer"]
    output_filename = "test_compile_ls.out"

    pipeline.compile(compilation_path, code_params, output_filename=output_filename)

    with open(output_filename, "rb") as f:
        compiled_circuit = pickle.load(f)
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
    compilation_path = ["PyZXLayer", "TopologiqLayer", "TQECLayer"]
    args_dict = {
        "TopologiqLayer": {"max_attempts": 1, "seed": 42},
    }
    output_filename = "test_compile_args.out"

    try:
        pipeline.compile(
            compilation_path, code_params, args_dict, output_filename=output_filename
        )
        with open(output_filename, "rb") as f:
            compiled_circuit = pickle.load(f)
        print(compiled_circuit)
    except Exception as err:
        assert str(err)[:19] == "Topologiq timed out"

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
    compilation_path = ["QiskitPBCLayer", "QiskitBicycleLayer"]
    args_dict = {
        "QiskitPBCLayer": {"fix_clifford": False},
    }

    # run pipeline
    pipeline.compile(
        compilation_path=compilation_path, compile_args=args_dict
    )  # this should raise a Runtime Warning

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
    compilation_path = ["PyZXLayer", "TQECLayer"]

    # This should do pathfinding to find TopologiqLayer connecting PyZXLayer with TQECLayer.
    pipeline.compile(compilation_path=compilation_path, code_params=code_params)

    return


def test_invalid_path():
    """
    In the event of some sort of invalid compilation path being provided, an informative error message should be given to the user and the tool should exit gracefully.
    """
    qc = QiskitCircuit(10)
    qc.h(0)
    qc.cx(0, 3)
    qc.cx(0, 4)
    qc.cx(0, 5)
    qc.cx(0, 6)
    qc.h(0)
    qc.h(1)

    pipeline = Pipeline(qc)
    # Clearly QiskitCircuit is not a layer and is not present in the compilation graph.
    compilation_path = ["TQECLayer", "QiskitCircuit"]

    try:
        pipeline.compile(compilation_path)
    except Exception as err:
        assert (
            str(err)
            == "One of the nodes specified in the compilation path does not exist in ftcc. You may have a typo in a layer name, or you may be trying to use a tool which is not yet implemented in ftcc. To see a list of tools implemented in ftcc, print the compilation graph."
        )

    compilation_path = ["BaseLayer", "TQECLayer"]

    try:
        pipeline.compile(compilation_path)
    except Exception as err:
        # print(err)
        assert str(err)[:14] == "No path exists", f"Actual exception was {err}"
    return
