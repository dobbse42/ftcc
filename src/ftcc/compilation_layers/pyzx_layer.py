import pyzx as zx
from ftcc.compilation_layers.base_layer import BaseLayer
from pyzx.graph.base import BaseGraph
from pyzx import extract_circuit


class PyZXLayer(BaseLayer):
    """
    Expects to be initialized with the circuit in the PyZX Circuit IR. Creates a PyZX graph IR from this.
    """

    def __init__(self, input_circ, metadata):
        """
        Initializes a PyZX optimization compilation layer.
        """

        self.metadata = metadata

        if isinstance(input_circ, BaseGraph):
            self.graph = input_circ
        elif isinstance(input_circ, zx.Circuit):
            # self.circuit = input_circ
            self.graph = input_circ.to_graph()

        if "num_ancilla" not in self.metadata.keys():
            self.metadata["num_ancilla"] = 0

        """if 'initial_state' not in self.metadata.keys():
            # initialize all qubits to 0 ket
            self.graph.apply_state('0' * self.metadata['num_qubits'])"""

        # zero out the ancilla
        """self.graph.apply_effect(
            '0' * self.metadata['num_ancilla']
            + '/' * (self.metadata['num_qubits'] - self.metadata['num_ancilla'])
        )"""

    def compile(self):
        """
        Applies optimizations on a PyZX graph.
        """

        zx.full_reduce(self.graph)
        # zx.to_rg(self.graph)

        return

    def output(self, output_IR="circuit"):
        """
        Returns the circuit in the PyZX Circuit IR by default, and the PyZX graph IR optionally. Also returns
        all metadata passed in.
        """

        if output_IR == "circuit":
            self.circuit = extract_circuit(self.graph)

        to_be_returned = {
            "IR": self.graph if output_IR == "graph" else self.circuit,
            "metadata": self.metadata,
        }

        return to_be_returned
