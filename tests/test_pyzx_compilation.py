import pytest
import pyzx as zx
import numpy as np
from qiskit import QuantumCircuit as QiskitCircuit
from qiskit import qasm2
from pyzx.generate import CNOT_HAD_PHASE_circuit, cliffordT

from ftcc.compilation_layers.pyzx_layer import PyZXLayer


def random_area_law_circuit(N, seed=42):
    """
    An example qiskit circuit acting over N qubits.
    Function adapted from that used in ucc's compile() tests.
    """
    state = np.random.rand(2**N) + 1j * np.random.rand(2**N)
    state /= np.linalg.norm(state)

    circuit = QiskitCircuit(N)
    circuit.initialize(state, range(N))
    qasm_circuit = qasm2.dumps(circuit)
    zx_circuit = zx.Circuit.from_qasm(qasm_circuit)

    return zx_circuit


"""@pytest.mark.parametrize("N", [3, 5, 7])
@pytest.mark.parametrize("circuit_type", ["cnot_had_phase"])
def test_zx_graph_correctness_small(N, circuit_type):
  # For num_qubits <= 10.

  #circuit = random_area_law_circuit(N)
  if circuit_type == "clifford_T":
    circuit = cliffordT(N, N**2)
  elif circuit_type == "cnot_had_phase":
    circuit = CNOT_HAD_PHASE_circuit(N, N**2)
  else:
    raise ValueError

  metadata = {}

  pyzx_layer = PyZXLayer(circuit, metadata)
  # converted_circuit = zx.Circuit.from_graph(pyzx_layer.graph)
  converted_circuit = pyzx_layer.output(output_IR="circuit")["IR"]

  # assert converted_circuit.verify_equality(circuit)
  assert zx.compare_tensors(circuit, converted_circuit)

  return"""


"""@pytest.mark.parametrize("N", [10])
@pytest.mark.parametrize("circuit_type", ["cnot_had_phase"])
def test_zx_graph_correctness_large(N, circuit_type):
  # For 10 < num_qubits < 50

  if circuit_type == "clifford_T":
    circuit = cliffordT(N, N**2)
  elif circuit_type == "cnot_had_phase":
    circuit = CNOT_HAD_PHASE_circuit(N, N**2)
  else:
    raise ValueError
  # circuit = random_area_law_circuit(N)
  metadata = {}

  pyzx_layer = PyZXLayer(circuit, metadata)
  # converted_circuit = zx.extract_circuit(pyzx_layer.graph)
  converted_circuit = pyzx_layer.output(output_IR="circuit")["IR"]

  # assert converted_circuit.verify_equality(circuit)
  assert zx.compare_tensors(circuit, converted_circuit)

  return"""


@pytest.mark.parametrize("N", [3, 5, 7])
@pytest.mark.parametrize("circuit_type", ["cnot_had_phase"])
def test_zx_optimized_correctness_small(N, circuit_type):
    # circuit = random_area_law_circuit(N)
    if circuit_type == "clifford_T":
        circuit = cliffordT(N, N**2)
    elif circuit_type == "cnot_had_phase":
        circuit = CNOT_HAD_PHASE_circuit(N, N**2)
    else:
        raise ValueError
    metadata = {}

    pyzx_layer = PyZXLayer(circuit, metadata)
    pyzx_layer.compile()
    # converted_circuit = zx.extract_circuit(pyzx_layer.graph)
    # converted_circuit = zx.Circuit.from_graph(pyzx_layer.graph)
    converted_circuit = pyzx_layer.output(output_IR="circuit")["IR"]

    assert zx.compare_tensors(circuit, converted_circuit)
    # assert converted_circuit.verify_equality(circuit)

    return


@pytest.mark.parametrize("N", [10, 12, 14])
@pytest.mark.parametrize("circuit_type", ["cnot_had_phase"])
def test_zx_optimized_correctness_large(N, circuit_type):
    # circuit = random_area_law_circuit(N)
    if circuit_type == "clifford_T":
        circuit = cliffordT(N, N**2)
    elif circuit_type == "cnot_had_phase":
        circuit = CNOT_HAD_PHASE_circuit(N, N**2)
    else:
        raise ValueError
    metadata = {}

    pyzx_layer = PyZXLayer(circuit, metadata)
    pyzx_layer.compile()
    # converted_circuit = zx.extract_circuit(pyzx_layer.graph)
    converted_circuit = pyzx_layer.output(output_IR="circuit")["IR"]

    # assert converted_circuit.verify_equality(circuit)
    assert zx.compare_tensors(circuit, converted_circuit)

    return
