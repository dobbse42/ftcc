__all__ = [
    "MQTEncodingLayer",
    "PyZXLayer",
    "TopologiqLayer",
    "TQECLayer",
    "UCCLayer",
    "NWQECPauliLayer",
    "NWQECTranspilationLayer",
]


def __getattr__(name):
    if name == "MQTEncodingLayer":
        from .mqt_encoding_layer import MQTEncodingLayer
    if name == "PyZXLayer":
        from .pyzx_layer import PyZXLayer
    if name == "TopologiqLayer":
        from .topologiq_layer import TopologiqLayer
    if name == "TQECLayer":
        from .tqec_layer import TQECLayer
    if name == "UCCLayer":
        from .ucc_layer import UCCLayer
    if name == "NWQECPauliLayer":
        from .nwqec_layer import NWQECPauliLayer
    if name == "NWQECTranspilationLayer":
        from .nwqec_layer import NWQECTranspilationLayer
    raise AttributeError(f"module {__name__} has no attribute {name}")
