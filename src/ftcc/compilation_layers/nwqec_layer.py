import nwqec
from ftcc.compilation_layers.base_layer import BaseLayer

import io
import contextlib
import tempfile


class NWQECPauliLayer(BaseLayer):
    def __init__(self, circuit, metadata):
        self.circuit = circuit
        self.metadata = metadata
        self.VALID_START_NODE = False

    @classmethod
    def set_compile_args(cls, flags, compile_args):
        return compile_args

    @classmethod
    def compilation_flags(cls):
        compilation_flags = {}
        return compilation_flags

    def compile(self, eps=1e-6, fuse_t=False):
        """Unfortunately it is necessary to do weird stdout capture to catch any runtime errors
        since the C++ errors in nwqec are not properly exposed in python yet.
        """
        self.circuit = nwqec.to_pbc(self.circuit, optimize_t_count=fuse_t, epsilon=eps)

        return


class NWQECTranspilationLayer(BaseLayer):
    def __init__(self, circuit, metadata):
        # assumes any strings passed are qasm strings. TODO: optionally accept qasm filenames?
        if isinstance(circuit, str):
            # print("circuit str: ", circuit)
            with tempfile.NamedTemporaryFile(mode="w+") as tmp:
                tmp.write(circuit)
                # print("tempfile contents: ")
                tmp.read()
                # print("everything else: ")
                self.circuit = nwqec.load_qasm(
                    tmp.name
                )  # nwqec only reads qasm files, not strings.
        else:  # circuit is an nwqec circuit already
            self.circuit = circuit
        self.metadata = metadata

    @classmethod
    def set_compile_args(cls, flags, compile_args):
        return compile_args

    @classmethod
    def compilation_flags(cls):
        compilation_flags = {}
        return compilation_flags

    def compile(self, keep_ccx: bool = False, eps: float = 1e-6):
        self.circuit = nwqec.to_clifford_t(self.circuit, keep_ccx=keep_ccx, epsilon=eps)

        return
