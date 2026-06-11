import importlib

"""from .compilation_layers import (
    BaseLayer,
    QiskitPBCLayer,
    QiskitBicycleLayer,
    TQECLayer,
    TopologiqLayer,
    PyZXLayer,
    MQTEncodingLater,
    NWQECTranspilationLayer,
    NWQECPauliLayer,
)"""

compilation_registry = {
    "BaseLayer": "ftcc.compilation_layers:BaseLayer",
    "QiskitPBCLayer": "ftcc.compilation_layers:QiskitPBCLayer",
    "QiskitBicycleLayer": "ftcc.compilation_layers:QiskitBicycleLayer",
    "TQECLayer": "ftcc.compilation_layers:TQECLayer",
    "TopologiqLayer": "ftcc.compilation_layers:TopologiqLayer",
    "PyZXLayer": "ftcc.compilation_layers:PyZXLayer",
    "MQTEncodingLayer": "ftcc.compilation_layers:MQTEncodingLayer",
    "NWQECTranspilationLayer": "ftcc.compilation_layers:NWQECTranspilationLayer",
    "NWQECPauliLayer": "ftcc.compilation_layers:NWQECPauliLayer",
}


def load_compilation_layer(label):
    path = compilation_registry[label]
    module_name, class_name = path.split(":")
    module = importlib.import_module(module_name)

    return getattr(module, class_name)
