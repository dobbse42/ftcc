from ftcc import CompilationGraph
from ftcc.translation_registry import translation_dictionary
import networkx as nx
from collections import deque


class Pipeline:
    """
    This is the primary way users will interface with ftcc.
    Users should be able to see compilation options for a particular circuit before
    performing any actual compilation.
    The minimum amount of information to run this is a circuit to compile and a way to infer
    a compilation path.
    The minimum specification required from a user is then 1) a circuit to be compiled, and
    2) a device to be compiled to or final node to run. The compilation path can be inferred
    from either of these two pieces of information.
    Optional specifications, which will be implemented later: constraints on the compilation
    path or compiled circuit.
    """

    def __init__(self, circuit, device=None, final_node=None):
        self.circuit = circuit
        self.compilation_graph = CompilationGraph()
        if device is not None:
            # TODO: encode constraints due to device
            # infer final node if not specified
            # if final_node is None:
            #     self.end_node = device_IRs[device]
            raise NotImplementedError
        if final_node is not None:
            self.end_node = final_node

    def compile(self, compilation_path=None, code_params=None, compile_args=None):
        """
        A compilation path is a list of tuples of compilation layers and arguments for their compile() calls.
        """
        if compilation_path is None:
            compilation_path = self.find_compilation_path()
        if compile_args is None:
            compile_args = {}

        # check that compilation path is valid
        for i, (layer, successor) in enumerate(
            zip(compilation_path, compilation_path[1:])
        ):
            valid_step = successor in self.compilation_graph.graph.neighbors(layer)
            if not valid_step:
                intermediate_path = self.find_path(layer, successor)
                compilation_path = (
                    compilation_path[:i] + intermediate_path + compilation_path[i:]
                )

        args_dict = self.get_compile_args(compilation_path, compile_args)

        """successor = compilation_path[-1]
    for layer, rev_i in enumerate(reverse(compilation_path[:-1])):
      valid_step = (successor in compilation_path.neighbors(layer))
      # if compilation path is not valid, do pathfinding for missing links
      if not valid_step:
        intermediate_path = find_path(layer, successor)
        compilation_path = compilation_path[:-rev_i] + intermediate_path + compilation_path[-rev_i:]
      successor = layer"""

        # set up metadata
        metadata = {}
        if code_params is None:
            # TODO: choose code from among those supported by all steps in the pipeline and within constraints
            # PLACEHOLDER: default to Gross code
            metadata["code_n"] = 144
            metadata["code_k"] = 12
            metadata["code_d"] = 12
            metadata["code_name"] = "gross"
        else:
            metadata["code_n"] = code_params["n"]
            metadata["code_k"] = code_params["k"]
            metadata["code_d"] = code_params["d"]
        # set up the first layer
        layer_type = compilation_path[0]
        layer = layer_type(self.circuit, metadata)

        # call each compilation layer and translation layer with appropriate args, returning any exceptions raised
        for successor in compilation_path[1:]:
            # print("layer: ", layer)
            layer.compile_args = args_dict[
                layer_type
            ]  # I don't like that this directly mutates properties of the object
            layer.compile()
            layer = translation_dictionary[layer_type, successor](layer)
            layer_type = successor
        layer.compile()
        # return the compiled circuit
        compiled_circuit = layer.circuit
        return compiled_circuit

    def get_compile_args(self, compilation_path, compile_args):
        # initialize default flag dict, all are False by default
        # TODO: refactor to import this from elsewhere and automate the addition of new flags
        flags = {
            "needs_unfixed_cliffords": False,
            "use_fixed_seed": False,
            "use_more_attempts": False,
        }
        args_dict = {}
        for layer in compilation_path:
            args_dict[layer] = {}

        args_dict.update(compile_args)  # set user-specified compilation args
        # TODO: check that all user-specified compile_args are real compilation args. This will avoid typos, etc.

        # check compile_args flags along the path
        for layer in reversed(compilation_path):
            # update required compilation args
            # args_dict.update({layer: layer.set_compile_args(flags)})
            # print("layer args before: ", args_dict[layer])
            layer.set_compile_args(flags, args_dict[layer])
            # print("layer args after: ", args_dict[layer])
            flags.update(
                layer.compilation_flags()
            )  # for now only let flags affect predecessors, check back to front.
            # print("flags: ", flags)
        return args_dict

    def find_compilation_graph(self):
        return self.find_path(self.start_node, self.end_node)

    def find_path(self, start, end):
        """
        For now this is done very simply since the graph is small.
        Returns: list of connected nodes with start at the 0th index and end at the -1th index.
        """
        return nx.shortest_path(self.compilation_graph.graph, source=start, target=end)
