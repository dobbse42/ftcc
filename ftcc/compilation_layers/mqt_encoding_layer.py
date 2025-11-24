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


    def compile(self):
        """
        Get an encoding circuit for the Steane code.
        """

        steane_code = CSSCode.from_code_name("Steane")
        self.circuit, self.metadata["registers"] = depth_optimal_encoding_circuit(steane_code, max_timeout=5)

        return
