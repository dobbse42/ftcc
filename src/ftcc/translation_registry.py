"""from .compilation_layers import (
    QiskitPBCLayer,
    QiskitBicycleLayer,
    TopologiqLayer,
    TQECLayer,
    PyZXLayer,
    MQTEncodingLayer,
    NWQECTranspilationLayer,
    NWQECPauliLayer,
)"""

"""from .translation_layers.qiskit_pbc_to_bicycle import (
    translate_qiskit_pbc_to_bicycle,
)
from .translation_layers.pyzx_to_topologiq import translate_pyzx_to_topologiq
from .translation_layers.topologiq_to_tqec import translate_topologiq_to_tqec
from .translation_layers.mqt_to_topologiq import translate_mqt_encoding_to_topologiq
from .translation_layers.nwqec_to_qiskit_bicycle import (
    translate_nwqec_to_qiskit_bicycle,
)
from .translation_layers.nwqec_transpilation_to_pauli import (
    translate_nwqec_transpilation_to_pauli,
)"""

translation_dictionary = {
    ("QiskitPBCLayer", "QiskitBicycleLayer"): "translate_qiskit_pbc_to_bicycle",
    ("PyZXLayer", "TopologiqLayer"): "translate_pyzx_to_topologiq",
    ("TopologiqLayer", "TQECLayer"): "translate_topologiq_to_tqec",
    ("MQTEncodingLayer", "TopologiqLayer"): "translate_mqt_encoding_to_topologiq",
    ("NWQECPauliLayer", "QiskitBicycleLayer"): "translate_nwqec_to_qiskit_bicycle",
    (
        "NWQECTranspilationLayer",
        "NWQECPauliLayer",
    ): "translate_nwqec_transpilation_to_pauli",
}


def __getattr__(name):
    if name == "translate_qiskit_pbc_to_bicycle":
        from .translation_layers.qiskit_pbc_to_bicycle import (
            translate_qiskit_pbc_to_bicycle,
        )

        return translate_qiskit_pbc_to_bicycle
    if name == "translate_pyzx_to_topologiq":
        from .translation_layers.pyzx_to_topologiq import translate_pyzx_to_topologiq

        return translate_pyzx_to_topologiq
    if name == "translate_topologiq_to_tqec":
        from .translation_layers.topologiq_to_tqec import translate_topologiq_to_tqec

        return translate_topologiq_to_tqec
    if name == "translate_mqt_encoding_to_topologiq":
        from .translation_layers.mqt_to_topologiq import (
            translate_mqt_encoding_to_topologiq,
        )

        return translate_mqt_encoding_to_topologiq
    if name == "translate_nwqec_to_qiskit_bicycle":
        from .translation_layers.nwqec_to_qiskit_bicycle import (
            translate_nwqec_to_qiskit_bicycle,
        )

        return translate_nwqec_to_qiskit_bicycle
    if name == "translate_nwqec_transpilation_to_pauli":
        from .translation_layers.nwqec_transpilation_to_pauli import (
            translate_nwqec_transpilation_to_pauli,
        )

        return translate_nwqec_transpilation_to_pauli


def load_translation_layer(label):
    return __getattr__(label)
