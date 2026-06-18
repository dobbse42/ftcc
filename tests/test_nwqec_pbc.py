import pytest
import nwqec
from qiskit.circuit.random import random_circuit, random_clifford_circuit
from qiskit import qasm2

import os
import sys
import tempfile
import ctypes

from ftcc.compilation_layers.nwqec_layer import NWQECPauliLayer
from ftcc.translation_layers.nwqec_to_qiskit_bicycle import (
    translate_nwqec_to_qiskit_bicycle,
)

pytestmark = pytest.mark.build

allowed_nwqec_cliffords = ["h", "x", "y", "z", "cx", "s", "sdg", "sx", "sxdg"]


@pytest.mark.parametrize("N", [3, 5, 7, 9, 11])
def test_fuse_t(N: int):
    qiskit_circuit = random_clifford_circuit(
        N, N**2, gates=allowed_nwqec_cliffords, seed=42
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".qasm") as tmp:
        qasm2.dump(qiskit_circuit, tmp.name)
        nwqec_circuit = nwqec.load_qasm(tmp.name)

    metadata = {}
    nwqec_pbc_layer = NWQECPauliLayer(nwqec_circuit, metadata=metadata)
    nwqec_fuse_layer = NWQECPauliLayer(nwqec_circuit, metadata=metadata)

    # print(nwqec_pbc_layer.circuit.to_qasm_str())

    nwqec_pbc_layer.compile(fuse_t=False)
    nwqec_fuse_layer.compile(fuse_t=True)

    assert nwqec_fuse_layer.circuit.count_ops().get(
        "t_pauli", 0
    ) <= nwqec_pbc_layer.circuit.count_ops().get("t_pauli", 0)

    print(nwqec_fuse_layer.circuit.count_ops())

    return


@pytest.mark.parametrize("N", [3, 5, 7, 9, 11])
def test_pbc__returns_only_m_paulis(N: int):
    qiskit_circuit = random_clifford_circuit(
        N, N**2, gates=allowed_nwqec_cliffords, seed=42
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".qasm") as tmp:
        qasm2.dump(qiskit_circuit, tmp.name)
        nwqec_circuit = nwqec.load_qasm(tmp.name)

    metadata = {}
    nwqec_pbc_layer = NWQECPauliLayer(nwqec_circuit, metadata=metadata)
    nwqec_fuse_layer = NWQECPauliLayer(nwqec_circuit, metadata=metadata)

    nwqec_pbc_layer.compile(fuse_t=False)
    nwqec_fuse_layer.compile(fuse_t=True)

    print(nwqec_fuse_layer.circuit.count_ops())
    print(nwqec_pbc_layer.circuit.count_ops())
    assert nwqec_fuse_layer.circuit.count_ops().keys() == {"m_pauli": 0}.keys()
    assert nwqec_pbc_layer.circuit.count_ops().keys() == {"m_pauli": 0}.keys()

    return


@pytest.mark.parametrize("N", [5])
def test_nwqec_to_bicycle(N: int):
    metadata = {
        "code_name": "gross",
        "code_n": 144,
        "code_k": 12,
        "code_d": 12,
    }

    qiskit_circuit = random_clifford_circuit(
        N, N**2, gates=allowed_nwqec_cliffords, seed=42
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".qasm") as tmp:
        qasm2.dump(qiskit_circuit, tmp.name)
        nwqec_circuit = nwqec.load_qasm(tmp.name)

    nwqec_layer = NWQECPauliLayer(circuit=nwqec_circuit, metadata=metadata)
    nwqec_layer.compile(fuse_t=False)

    bicycle_layer = translate_nwqec_to_qiskit_bicycle(nwqec_layer)
    bicycle_layer.compile()

    print(bicycle_layer.circuit)

    return
