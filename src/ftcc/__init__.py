__all__ = ["MQTEncodingLayer", "PyZXLayer", "TopologiqLayer", "TQECLayer", "UCCLayer"]

from .compilation_graph import (
    CompilationGraph as CompilationGraph,
)


def __getattr__(name):
    if name == "MQTEncodingLayer":
        from .compilation_layers.mqt_encoding_layer import MQTEncodingLayer
    if name == "PyZXLayer":
        from .compilation_layers.pyzx_layer import PyZXLayer
    if name == "TopologiqLayer":
        from .compilation_layers.topologiq_layer import TopologiqLayer
    if name == "TQECLayer":
        from .compilation_layers.tqec_layer import TQECLayer
    if name == "UCCLayer":
        from .compilation_layers.ucc_layer import UCCLayer
    raise AttributeError(f"module {__name__} has no attribute {name}")
