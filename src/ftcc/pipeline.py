from ftcc import CompilationGraph
from ftcc.get_requirements import get_requirements
import networkx as nx
from collections import deque
import os
import subprocess
import pickle
import json


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
            raise NotImplementedError(
                "Device-specific compilation is not yet supported. Try again without specifying a device."
            )
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

        # args_dict = self.get_compile_args(compilation_path, compile_args) # this is now done at compile-time

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
            metadata["code_name"] = (
                code_params["name"]
                if "name" in code_params.keys()
                else "unknown_code_name"
            )
        # get dependency list
        get_requirements(compilation_path)
        # ---- breakpoint if user wants to handle environment setup themselves ----
        # all names should be based on name information in metadata..
        config_filename = "placeholder_config_name.json"
        circuit_filename = "placeholder_circuit_name.pkl"
        requirements_filename = "compilation_requirements.txt"
        venv_name = "placeholder_venv_name"
        output_filename = "placeholder_output_name.pkl"

        # create venv
        subprocess.run(["uv", "venv", venv_name], check=True)
        # install dependencies
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--python",
                venv_name,
                "-r",
                requirements_filename,
            ],
            check=True,
        )
        # subprocess.run(["uv", "pip", "install", "--python", venv_name, "."], check=True) # install ftcc
        config = {
            "circuit_filename": circuit_filename,
            "compilation_path": compilation_path,
            "metadata": metadata,
            "compile_args": compile_args,
            "output_filename": output_filename,
        }

        # dump circuit info
        with open(circuit_filename, "wb") as f:
            pickle.dump(self.circuit, f)
        # dump config info
        with open(config_filename, "w") as f:
            f.write(json.dumps(config))

        # ---- breakpoint if user wants to do the compilation themselves ----
        # run compilation
        subprocess.run(
            [
                "uv",
                "run",
                "--python",
                venv_name,
                "python",
                "-m",
                "ftcc.run_with_venv",
                config_filename,
            ],
            check=True,
        )

        print("compilation run complete")
        with open(output_filename, "rb") as f:
            compiled_circuit = pickle.load(f)
        print(compiled_circuit)
        return

    """def get_compile_args(self, compilation_path, compile_args):
        # initialize default flag dict, all are False by default
        # TODO: refactor to import this from elsewhere and automate the addition of new flags
        flags = {
            'needs_unfixed_cliffords': False,
            'use_fixed_seed': False,
            'use_more_attempts': False,
        }
        args_dict = {}
        for layer in compilation_path:
            args_dict[layer] = {}

        args_dict.update(compile_args)  # set user-specified compilation args
        # TODO: check that all user-specified compile_args are real compilation args. This will avoid typos, etc.

        # check compile_args flags along the path
        for layer_name in reversed(compilation_path):
            layer = compilation_registry[layer_name]
            # update required compilation args
            # args_dict.update({layer: layer.set_compile_args(flags)})
            # print('layer args before: ', args_dict[layer])
            layer.set_compile_args(flags, args_dict[layer_name])
            # print('layer args after: ', args_dict[layer])
            flags.update(
                layer.compilation_flags()
            )  # for now only let flags affect predecessors, check back to front.
            # print('flags: ', flags)
        return args_dict"""

    def find_compilation_path(self):
        return self.find_path(self.start_node, self.end_node)

    def find_path(self, start, end):
        """
        For now this is done very simply since the graph is small.
        Returns: list of connected nodes with start at the 0th index and end at the -1th index.
        """
        try:
            path = nx.shortest_path(
                self.compilation_graph.graph, source=start, target=end
            )
        except nx.exception.NodeNotFound:
            raise NotImplementedError(
                "One of the nodes specified in the compilation path does not exist in ftcc. You may have a typo in a layer name, or you may be trying to use a tool which is not yet implemented in ftcc. To see a list of tools implemented in ftcc, print the compilation graph."
            )
        except nx.exception.NetworkXNoPath:
            raise RuntimeError(
                f"No path exists between the specified nodes {start} and {end}."
            )
        return path
