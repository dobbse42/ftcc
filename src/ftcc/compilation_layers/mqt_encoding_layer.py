from ftcc.compilation_layers.base_layer import BaseLayer

from mqt.qecc.circuit_synthesis import depth_optimal_encoding_circuit
from mqt.qecc import CSSCode


class MQTEncodingLayer(BaseLayer):
    """
    Layer to get an encoding circuit for the Steane code from the Munich Quantum Toolkit (MQT).
    Should be expanded to get encoding circuits for multiple different codes. Currently always a start node.
    """

    def __init__(self, metadata):
        """
        aa
        """

        self.metadata = metadata
        self.mqt_code = CSSCode.from_code_name(self.metadata["code_name"])

    def compile(self):
        """
        Get an encoding circuit for the Steane code.
        """

        # steane_code = CSSCode.from_code_name("Steane")
        # qec_code = CSSCode.from_code_name(self.metadata['code_name'])
        self.circuit, _ = depth_optimal_encoding_circuit(self.mqt_code, max_timeout=5)

        self.metadata["num_qubits"] = self.circuit.num_qubits
        self.metadata["num_ancilla"] = (
            self.metadata["num_qubits"] - self.metadata["code_n"]
        )

        return
