Translation Layers

This is where most of the development effort for creating new layers goes, hence it gets its own dedicated page and explanation. At the moment, translation layers are a single function each, where each layer gets a dedicated file. This isolation is largely to avoid potential dependency conflicts. At the moment, edges in the compilation graph have a one-to-one correspondence with translation layers. Whether this will remain the case in the future is an open question, but the reasoning for the current decision is that rather than spending development time trying to force the outputs of compilation layers into certain standard IRs (and potentially losing information or limiting the compilation outputs of these layers), we take advantage of the relatively small size of the compilation graph and write a tailored translation layer for every edge. If a tool naturally lends itself to a standard IR, then this just results in a short and easy-to-write translation layer.

## Cardinal rules:
- **No compilation**: Translation functions should not perform any actual compilation. If there is some amount of compilation work necessary to link two steps of the pipeline together, please write and publish code performing this compilation as a separate tool which can then be integrated into `ftcc` as a new layer.
- **Isolation**: Translation functions should only call either the preceding or succeeding compilation layers, even if this means duplicating code from another compilation or translation layer. Calls to external libraries are of course allowed and encouraged.


## Some subtleties:
- Passing through intermediate IRs in order to get the output of the preceding layer into an IR compatible with the succeeding layer is totally fine. e.g. PyZX and qasm are common input IRs, so it is typical to see a translation function which converts output to a ZX-graph in PyZX to be provided as input to the next layer, even if the PyZX layer itself is not event present in the compilation pipeline.
- Most tools in the library are either written in python or have python APIs, but this is not universally true. It is totally permissible for a translation layer to involve shell scripts
- Technically a translation function should only need to import the succeeding compilation layer and not the preceding one. This is not a firm rule, it is just how most translation layers end up being structured. This may later become a cardinal rule if we need to handle dependency conflicts between succeeding tools.
