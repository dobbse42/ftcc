__all__ = [
    "MQTEncodingLayer",
    "PyZXLayer",
    "TopologiqLayer",
    "TQECLayer",
    "UCCLayer",
    "NWQECPauliLayer",
    "QiskitPBCLayer",
    "QiskitBicycleLayer",
]


def __getattr__(name):
    if name == "MQTEncodingLayer":
        from .mqt_encoding_layer import MQTEncodingLayer

        return MQTEncodingLayer
    if name == "PyZXLayer":
        from .pyzx_layer import PyZXLayer

        return PyZXLayer
    if name == "TopologiqLayer":
        from .topologiq_layer import TopologiqLayer

        return TopologiqLayer
    if name == "TQECLayer":
        from .tqec_layer import TQECLayer

        return TQECLayer
    if name == "UCCLayer":
        from .ucc_layer import UCCLayer

        return UCCLayer
    if name == "NWQECPauliLayer":
        from .nwqec_layer import NWQECPauliLayer

        return NWQECPauliLayer
    if name == "QiskitPBCLayer":
        from .qiskit_layer import QiskitPBCLayer

        return QiskitPBCLayer
    if name == "QiskitBicycleLayer":
        from .qiskit_layer import QiskitBicycleLayer

        return QiskitBicycleLayer
    raise AttributeError(f"module {__name__} has no attribute {name}")
