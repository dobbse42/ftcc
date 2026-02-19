import nwqec
from ftcc.compilation_layers.base_layer import BaseLayer

import io
import contextlib


class NWQECPauliLayer(BaseLayer):
    def __init__(self, circuit, metadata):
        self.circuit = circuit
        self.metadata = metadata

    def compile(self, eps=1e-6, fuse_t=False):
        """Unfortunately it is necessary to do weird stdout capture to catch any runtime errors
        since the C++ errors in nwqec are not properly exposed in python yet.
        """
        self.circuit = nwqec.to_pbc(self.circuit, optimize_t_count=fuse_t, epsilon=eps)

        return
