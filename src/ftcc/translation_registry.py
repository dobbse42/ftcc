from .compilation_layers import (
    QiskitPBCLayer,
    QiskitBicycleLayer,
    TopologiqLayer,
    TQECLayer,
    PyZXLayer,
    MQTEncodingLayer,
)

from .translation_layers.qiskit_pbc_to_bicycle import (
    translate_qiskit_pbc_to_bicycle,
)
from .translation_layers.pyzx_to_topologiq import translate_pyzx_to_topologiq
from .translation_layers.topologiq_to_tqec import translate_topologiq_to_tqec
from .translation_layers.mqt_to_topologiq import translate_mqt_encoding_to_topologiq

translation_dictionary = {
    (QiskitPBCLayer, QiskitBicycleLayer): translate_qiskit_pbc_to_bicycle,
    (PyZXLayer, TopologiqLayer): translate_pyzx_to_topologiq,
    (TopologiqLayer, TQECLayer): translate_topologiq_to_tqec,
    (MQTEncodingLayer, TopologiqLayer): translate_mqt_encoding_to_topologiq,
}
