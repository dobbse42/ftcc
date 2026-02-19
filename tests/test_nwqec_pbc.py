import pytest
import nwqec
from qiskit.circuit.random import random_circuit, random_clifford_circuit
from qiskit import qasm2

import os
import sys
import tempfile
import ctypes

from ftcc.compilation_layers.nwqec_layer import NWQECPauliLayer
from ftcc.compilation_layers.mqt_encoding_layer import MQTEncodingLayer

from ftcc.translation_layers.mqt_to_nwqec import translate_mqt_to_nwqec


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

    return


def test_mqt_nwqec():
    metadata = {
        "code_n": 7,
        "code_k": 1,
        "code_d": 3,
        "code_name": "Steane",
    }

    mqt_layer = MQTEncodingLayer(metadata=metadata)
    mqt_layer.compile()

    nwqec_layer = translate_mqt_to_nwqec(mqt_layer)

    nwqec_layer.compile()
    # print(nwqec_layer.circuit.to_qasm_str())

    return
