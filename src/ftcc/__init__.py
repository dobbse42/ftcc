import importlib

from .compilation_graph import (
    CompilationGraph as CompilationGraph,
)

# from .compilation_layers import (
#     QiskitPBCLayer,
#     QiskitBicycleLayer,
# )

from .pipeline import Pipeline
from .get_requirements import get_requirements

"""def load_class(label):
    path = compilation_registry[label]
    module_name, class_name = path.split(':')
    module = importlib.import_module(module_name)
    return getattr(module, class_name)"""

# from .translation_registry import translation_dictionary

# from .translation_layers.qiskit_pbc_to_bicycle import (
#     translate_qiskit_pbc_to_bicycle,
# )
