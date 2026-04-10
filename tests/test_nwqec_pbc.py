import pytest
import nwqec
from qiskit.circuit.random import random_circuit, random_clifford_circuit
from qiskit import qasm2

import os
import sys
import tempfile
import ctypes

from ftcc.compilation_layers.nwqec_layer import NWQECPauliLayer


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
