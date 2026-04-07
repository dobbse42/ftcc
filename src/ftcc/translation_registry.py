from .compilation_layers import QiskitPBCLayer, QiskitBicycleLayer
from .translation_layers.qiskit_pbc_to_bicycle import (
    translate_qiskit_pbc_to_bicycle,
)

translation_dictionary = {
    (QiskitPBCLayer, QiskitBicycleLayer): translate_qiskit_pbc_to_bicycle,
}
