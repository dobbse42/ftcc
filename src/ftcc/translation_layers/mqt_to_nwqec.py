import nwqec
from qiskit import qasm2
import tempfile

from ftcc.compilation_layers.mqt_encoding_layer import MQTEncodingLayer
from ftcc.compilation_layers.nwqec_layer import NWQECPauliLayer


def translate_mqt_to_nwqec(mqt_layer: MQTEncodingLayer):
    """
    nwqec requires that input circuits be specified as qasm files specifically,
    so temp files are necessary.
    """

    # write the mqt circuit to a temp qasm file and load as an nwqec circuit
    with tempfile.NamedTemporaryFile() as tmp:
        qasm2.dump(mqt_layer.circuit, tmp.name)
        circuit = nwqec.load_qasm(tmp.name)

    # create nwqec layer
    nwqec_layer = NWQECPauliLayer(circuit, metadata=mqt_layer.metadata)

    return nwqec_layer
