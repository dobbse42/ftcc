import pyzx as zx
from topologiq.utils.interop_pyzx import pyzx_g_to_simple_g
from topologiq_layer import TopologiqLayer
from pyzx_layer import PyZXLayer

class PyZXToTopologiqTranslator(base_translation_layer.BaseTranslationLayer):
    """
    aa
    """

    def __init__(self):
        """
        aa
        """

        pass


    def translate(self, pyzx_layer):
        """
        aa
        """

        simple_graph = pyzx_g_to_simple_g(pyzx_layer.compiled_graph)
        topologiq_layer = TopologiqLayer(simple_graph)

        return topologiq_layer
