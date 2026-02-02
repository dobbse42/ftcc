from ftcc.compilation_layers.pyzx_layer import PyZXLayer
from ftcc.translation_layers.topologiq_to_tqec import translate_topologiq_to_tqec

# from ftcc.translation_layers.pyzx_to_topologiq import PyZXToTopologiqTranslator
from ftcc.translation_layers.pyzx_to_topologiq import translate_pyzx_to_topologiq

import qiskit.qasm2 as qasm2
from qiskit import QuantumCircuit
import pyzx as zx
from tqec.utils.enums import Basis

# Define encoding circuit for steane code. This is an example of something that could be convertd to an encoding circuit layer.

qc = QuantumCircuit(10)
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
zx_graph = zx_circuit.to_graph()

num_apply_state = zx_graph.num_inputs()
zx_graph.apply_state("0" * num_apply_state)
zx_graph.apply_effect("000///////")

# Use framework
metadata = {
    "code_n": 7,
    "code_k": 1,
    "code_d": 3,
}
pyzx_layer = PyZXLayer(zx_graph, metadata=metadata)
pyzx_layer.compile()

topologiq_layer = translate_pyzx_to_topologiq(pyzx_layer)
topologiq_layer.compile()

tqec_layer = translate_topologiq_to_tqec(topologiq_layer)
tqec_layer.compile(Basis.X)  # basis could also potentially be specified in metadata

print(tqec_layer.stim_circuit)
