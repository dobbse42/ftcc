from ftcc.translation_registry import translation_dictionary, load_translation_layer
from ftcc.compilation_registry import compilation_registry, load_compilation_layer
from ftcc import Pipeline

import pickle
import json


def get_compile_args(compilation_path, compile_args):
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
    for layer_name in reversed(compilation_path):
        layer = load_compilation_layer(layer_name)
        # update required compilation args
        # args_dict.update({layer: layer.set_compile_args(flags)})
        # print("layer args before: ", args_dict[layer])
        layer.set_compile_args(flags, args_dict[layer_name])
        # print("layer args after: ", args_dict[layer])
        flags.update(
            layer.compilation_flags()
        )  # for now only let flags affect predecessors, check back to front.
    # print("flags: ", flags)
    return args_dict


def compile_with_venv(config_filename):
    """
    This function is only meant to be called within a virtual environment by Pipeline.compile().
    It is assumed that this function is running within a virtual environment with all requiremets
    for the specified compilation path already installed.
    """

    # ---- load config ----
    with open(config_filename, "r") as f:
        config = json.load(f)
    # read circuit
    with open(config["circuit_filename"], "rb") as f:
        circuit = pickle.load(f)
    # read compilation path
    compilation_path = config["compilation_path"]
    # compilation_path = [val.strip()[1:-1] for val in config['compilation_path'][1:-1].split(', ')] # old version for strings
    # read compilation args
    # args_dict = config['args_dict']
    provided_compile_args = config["compile_args"]
    # read metadata
    metadata = config["metadata"]
    # output filename
    output_filename = config["output_filename"]

    # ---- compilation logic ----
    print("Getting compile args for compilation path")
    args_dict = get_compile_args(compilation_path, provided_compile_args)
    print(f"Now compiling with compilation path: {compilation_path}")

    # set up the first layer
    layer_type = compilation_path[0]
    layer = load_compilation_layer(layer_type)(circuit, metadata)
    # call each compilation layer and translation layer with appropriate args, returning any exceptions raised
    for successor in compilation_path[1:]:
        # print("layer: ", layer)
        layer.compile_args = args_dict[
            layer_type
        ]  # I don't like that this directly mutates properties of the object
        layer.compile()
        layer = load_translation_layer(translation_dictionary[layer_type, successor])(
            layer
        )
        layer_type = successor
    layer.compile()
    # return the compiled circuit
    compiled_circuit = layer.circuit

    # write compiled circuit to file
    with open(output_filename, "wb") as f:
        pickle.dump(compiled_circuit, f)
    return compiled_circuit


if __name__ == "__main__":
    import sys

    compile_with_venv(sys.argv[1])
