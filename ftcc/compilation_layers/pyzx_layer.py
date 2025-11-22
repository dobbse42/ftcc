import PyZX as zx

class PyzxOptimizerLayer(base_layer.BaseLayer):
    """
    Expects to be initialized with the circuit in the PyZX Circuit IR. Creates a PyZX graph IR from this.
    """

    def __init__(self, input_circ, metadata):
        """
        Initializes a PyZX optimization compilation layer.
        """
        if isinstance(input_circ, zx.Graph):
            self.graph = input_circ
            self.circuit = self.graph.to_circuit()
        elif isinstance(input_circ, zx.Circuit):
            self.circuit = input_circ
            self.graph = self.circuit.to_graph()



    def compile(self):
        """
        Applies optimizations on a PyZX graph.
        """

        zx.full_reduce(self.zx_graph)
        zx.to_rg(zx_graph)

        return


    def output(self, output_IR="circuit"):
        """
        Returns the circuit in the PyZX Circuit IR by default, and the PyZX graph IR optionally. Also returns
        all metadata passed in.
        """

        to_be_returned = {
            IR: self.graph if output_IR == "graph" else self.circuit,
            metadata: self.metadata,
            }
        
        return to_be_returned
