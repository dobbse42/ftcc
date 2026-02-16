from ftcc.compilation_layers.mqt_encoding_layer import MQTEncodingLayer
from ftcc.translation_layers.topologiq_to_tqec import translate_topologiq_to_tqec
from ftcc.translation_layers.pyzx_to_topologiq import translate_pyzx_to_topologiq
from ftcc.translation_layers.mqt_to_pyzx import translate_mqt_encoding_to_pyzx

from tqec.utils.enums import Basis

# Define encoding circuit for steane code. This is an example of something that could be convertd to an encoding circuit layer.

metadata = {
    "code_n": 7,
    "code_k": 1,
    "code_d": 3,
    "code_name": "Steane",
}
mqt_encoding_layer = MQTEncodingLayer(metadata=metadata)
mqt_encoding_layer.compile()

pyzx_layer = translate_mqt_encoding_to_pyzx(mqt_encoding_layer)
pyzx_layer.compile(apply_state=True, apply_effect=True)

topologiq_layer = translate_pyzx_to_topologiq(pyzx_layer)
topologiq_layer.compile()

tqec_layer = translate_topologiq_to_tqec(topologiq_layer)
tqec_layer.compile(Basis.X)  # basis could also potentially be specified in metadata

print(tqec_layer.stim_circuit)
