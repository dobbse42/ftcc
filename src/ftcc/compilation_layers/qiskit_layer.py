from ftcc.compilation_layers.base_layer import BaseLayer

import qiskit
from qiskit.transpiler.passes import LitinskiTransformation


class QiskitPBCLayer(BaseLayer):
    def __init__(self, circuit, metadata):
        self.metadata = metadata
        self.circuit = circuit

    def compile(self, fix_clifford=True):
        lit = LitinskiTransformation(fix_clifford=fix_clifford)
        self.circuit = lit(self.circuit)

        return
