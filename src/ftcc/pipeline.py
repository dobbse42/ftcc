from ftcc import CompilationGraph
from ftcc.get_requirements import get_requirements
from ftcc.compilation_registry import valid_start_nodes
import networkx as nx
from collections import deque
import os
import subprocess
import pickle
import json
from subprocess import CalledProcessError


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

    def compile(
        self,
        compilation_path=None,
        code_params=None,
        compile_args=None,
        manual_compile=False,
        requirements_filename=None,
        config_filename=None,
        circuit_filename=None,
        output_filename=None,
        print_output=False,
    ):
        """
        A compilation path is a list of tuples of compilation layers and arguments for their compile() calls.
        """

        requirements_filename = "compilation_requirements.txt"

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
                # print("not a valid step!")
                intermediate_path = self.find_path(layer, successor)
                # print(f"intermediate path is {intermediate_path}")
                compilation_path = (
                    compilation_path[:i] + intermediate_path + compilation_path[i:]
                )
        assert compilation_path[0] in valid_start_nodes, (
            f"{compilation_path[0]} is not a valid start node."
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
        get_requirements(compilation_path, requirements_filename)

        # all names should be based on name information in metadata..
        if config_filename is None:
            config_filename = "placeholder_config_name.json"
        if circuit_filename is None:
            circuit_filename = "placeholder_circuit_name.pkl"
        if output_filename is None:
            output_filename = "placeholder_output_name.pkl"

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
            try:
                pickle.dump(self.circuit, f)
            except TypeError:
                raise TypeError(
                    "Something went wrong when pickling the input circuit. Most likely you are passing the input circuit in a format which cannot be pickled. Check the accepted input formats of the first compilation layer in your compilation path and make sure you pass the input circuit in one of the formats which can be pickled."
                )
        # dump config info
        with open(config_filename, "w") as f:
            f.write(json.dumps(config))

        # ---- breakpoint if user wants to do the compilation themselves ----
        if manual_compile:
            print(
                f"Requirements contained in {requirements_filename}. Stopping here. Manual compilation can be performed by `uv run --with-requirements {requirements_filename} python -m ftcc.run_with_venv {config_filename}`"
            )
            return
        # run compilation
        try:
            subprocess.run(  # needs uv run --quiet if you want to do error passing
                [
                    "uv",
                    "run",
                    "--with-requirements",
                    requirements_filename,
                    "python",
                    "-m",
                    "ftcc.run_with_venv",
                    config_filename,
                ],
                check=True,
                capture_output=False,
            )
        except CalledProcessError as err:
            # print("CalledProcessError. stderr below:")
            # subprocess_exception = json.loads(err.stderr)
            # print(err.stderr)
            # print("exception type: ", subprocess_exception["type"])
            # print("exception message: ", subprocess_exception["message"])
            # print(err)
            raise err
            # raise RuntimeError("An exception occurred during compilation.")
            # TODO: log compilation error information

        print("compilation run complete")
        with open(output_filename, "rb") as f:
            compiled_circuit = pickle.load(f)
        if print_output:
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
        # print(f"finding path from {start} to {end}")
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
        except Exception as e:
            print("Got some unexpected exception.")
            raise e
        return path
