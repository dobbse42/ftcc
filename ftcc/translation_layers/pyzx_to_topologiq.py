import pyzx as zx
from topologiq.utils.interop_pyzx import pyzx_g_to_simple_g
from ftcc.compilation_layers.topologiq_layer import TopologiqLayer
from ftcc.compilation_layers.pyzx_layer import PyZXLayer


def translate_pyzx_to_topologiq(pyzx_layer):
    """
    Creates a TopologiqLayer object from a compiled PyZXLayer object.
    """
    
    simple_graph = pyzx_g_to_simple_g(pyzx_layer.graph)
    topologiq_layer = TopologiqLayer(simple_graph, metadata=pyzx_layer.metadata)

    return topologiq_layer
