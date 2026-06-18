import pytest
import tomllib
import subprocess

from ftcc.get_requirements import get_requirements
from ftcc import Pipeline

from qiskit import QuantumCircuit as QiskitCircuit
from qiskit.circuit.random import random_circuit
from qiskit import qasm2
import nwqec
import tempfile
import pyzx as zx


"""from ftcc.compilation_layers import (
    QiskitPBCLayer,
    QiskitBicycleLayer,
    MQTEncodingLayer,
    TopologiqLayer,
    TQECLayer,
    PyZXLayer,
    BaseLayer,
)"""

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
    qasm_str = qasm2.dumps(qiskit_circuit)

    return qasm_str


def test_build_info_correctness():
    filename = "src/ftcc/_build_info.toml"

    with open(filename, "rb") as f:
        build_info = tomllib.load(f)
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    # print(pyproject["dependency-groups"])

    # print(build_info["dependency-groups"])
    # print(build_info["dependency-conflicts"])
    # print(build_info["dependency-sources"])
    # print(pyproject.keys())

    assert build_info["dependency-groups"] == pyproject["dependency-groups"]
    assert build_info["dependency-sources"] == pyproject["tool"]["uv"]["sources"]
    assert build_info["dependency-conflicts"] == pyproject["tool"]["uv"]["conflicts"]
    return


def test_requirements_build_script():
    requirements_filename = "test_compile_requirements.txt"
    path = ["QiskitPBCLayer", "QiskitBicycleLayer"]
    get_requirements(path, requirements_filename)

    return


def test_compile_breakpoints():
    circuit = QiskitCircuit(10)
    # The circuit conetents do not matter
    circuit.h(0)
    circuit.cx(0, 3)
    circuit.cx(0, 4)
    circuit.cx(0, 5)
    circuit.cx(0, 6)
    circuit.h(0)
    circuit.h(1)
    pipeline = Pipeline(circuit)
    compilation_path = ["QiskitPBCLayer", "QiskitBicycleLayer"]
    output_filename = "breakpoint_test_output.out"
    pipeline.compile(
        compilation_path, manual_compile=True, output_filename=output_filename
    )
    try:
        with open(output_filename, "rb") as _:
            print("There was an output file.")
        subprocess.run("rm", output_filename)
        raise AssertionError("Breakpoint did not work.")

    except Exception as e:
        print(f"Got exception {e}")
        return

    return


def test_path_validity():
    circuit = QiskitCircuit(10)
    # The circuit conetents do not matter
    circuit.h(0)
    circuit.cx(0, 3)
    circuit.cx(0, 4)
    circuit.cx(0, 5)
    circuit.cx(0, 6)
    circuit.h(0)
    circuit.h(1)
    pipeline = Pipeline(circuit)
    compilation_path = ["TopologiqLayer", "QiskitPBCLayer"]
    try:
        pipeline.compile(compilation_path)
    except RuntimeError:
        return
    else:
        raise AssertionError("This compilation should have failed")
    return


def test_dependency_conflicts():
    compilation_path = ["TopologiqLayer", "QiskitPBCLayer"]
    requirements_filename = "dummy_test_requirements.txt"
    try:
        get_requirements(compilation_path, requirements_filename)
    except RuntimeError:
        return
    else:
        raise AssertionError("This compilation should have failed")
    return


def test_full_pipeline_nwqec():
    N = 5
    nwqec_circuit = generate_random_nwqec_circuit(N)
    pipeline = Pipeline(nwqec_circuit)
    compilation_path = [
        "NWQECTranspilationLayer",
        "NWQECPauliLayer",
        "QiskitBicycleLayer",
    ]
    pipeline.compile(compilation_path)
    return


def test_full_pipeline_lattice_surgery():
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

    qasm_str = qasm2.dumps(qc)
    # Make ready for PyZX layer (this would become a translation layer)
    zx_circuit = zx.Circuit.from_qasm(qasm_str)

    pipeline = Pipeline(zx_circuit)
    compilation_path = ["PyZXLayer", "TopologiqLayer", "TQECLayer"]
    pipeline.compile(compilation_path)

    return


def test_full_pipeline_qiskit():
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

    pipeline = Pipeline(qc)
    compilation_path = ["QiskitPBCLayer", "QiskitBicycleLayer"]

    # get path and compile
    pipeline.compile(compilation_path)

    return
