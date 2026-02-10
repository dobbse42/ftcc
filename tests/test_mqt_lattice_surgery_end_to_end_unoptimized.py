import pytest
from ftcc.compilation_layers.tqec_layer import TQECLayer
from ftcc.compilation_layers.topologiq_layer import TopologiqLayer
from ftcc.compilation_layers.mqt_encoding_layer import MQTEncodingLayer
from ftcc.translation_layers.topologiq_to_tqec import translate_topologiq_to_tqec
from ftcc.translation_layers.mqt_to_topologiq import translate_mqt_encoding_to_topologiq

import qiskit
import qiskit.qasm2 as qasm2
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
import pyzx as zx
from tqec.utils.enums import Basis

# Define encoding circuit for steane code. This is an example of something that could be convertd to an encoding circuit layer.

metadata = {"code_n": 7, "code_k": 1, "code_d": 3, "code_name": "Steane"}

mqt_encoding_layer = MQTEncodingLayer(metadata=metadata)
mqt_encoding_layer.compile()

topologiq_layer = translate_mqt_encoding_to_topologiq(mqt_encoding_layer)
topologiq_layer.compile()

tqec_layer = translate_topologiq_to_tqec(topologiq_layer)
tqec_layer.compile(Basis.X)  # basis could also potentially be specified in metadata

print(tqec_layer.stim_circuit)
