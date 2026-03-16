import qiskit
from qiskit import QuantumCircuit
import numpy as np
import json
from collections.abc import Iterator

from ftcc.compilation_layers.qiskit_layer import QiskitPBCLayer, QiskitBicycleLayer


def translate_qiskit_pbc_to_bicycle(pbc_layer: QiskitPBCLayer):
    """
    aa
    """

    metadata = pbc_layer.metadata

    pbc_iter = iter_qiskit_pbc_circuit(pbc_layer.circuit)
    circuit = "\n".join(map(json.dumps, pbc_iter))
    bicycle_layer = QiskitBicycleLayer(circuit, metadata)

    return bicycle_layer


def iter_qiskit_pbc_circuit(
    pbc: "QuantumCircuit", as_str: bool = False
) -> Iterator[dict] | Iterator[str]:
    """
    This method is taken almost identically from bicycle-architecture-compiler/scripts/qiskit_parser.py.
    Presumably at some point the python utilities within bicycle-architecture-compiler will be published
    as a PyPI package, at which point this method will be rewritten to just call the package. But until then,
    between adding the entire git repo as a dependency and simply copying a single method, we choose the latter
    (not to mention that the repo does not actually contain any __init__.py files for modules).
    Note that for our purposes it would be better if this yielded a json rather than an iterator which can be
    used to construct a json, but in anticipation of a published version of this function it is best not to
    modify its behavior.

    Begin original documentation:
    Yield PBC instructions consumable by the bicycle compiler.

    Args:
        pbc: The Qiskit ``QuantumCircuit`` object to iterate over. This circuit is required to
            be in PBC format, i.e. contain only ``PauliEvolutionGate`` objects with a single
            Pauli as operator, and ``PauliProductMeasurement`` instructions.
        as_str: If ``True``, yield instructions as string that's directly consumable by
            the ``bicycle_compiler`` executable. If ``False``, return the plain dictionary.

    Returns:
        An iterator over PBC instructions in the bicycle compilers JSON format, that is
        ``{"Rotation": {"basis": ["Z", "X", "Y", "I"], "angle": 0.123}}`` or
        ``{"Measurement": {"basis": ["Z", "X", "Y", "I"], "flipped": True}}``.
        If ``as_str`` is ``True``, the dictionaries are JSON serialized and whitespaces removed.

    Raises:
        ValueError: If the input circuit is not in the required PBC format.
    """

    PAULI_TABLE = {
        (True, True): "Y",
        (True, False): "Z",
        (False, True): "X",
        (False, False): "I",
    }

    qubit_to_index = {qubit: index for index, qubit in enumerate(pbc.qubits)}

    # potentially transform the instruction to string format
    if as_str:
        to_str = lambda inst: json.dumps(inst).replace(" ", "")
    else:
        to_str = lambda inst: inst  # no op

    for i, inst in enumerate(pbc.data):
        if inst.name == "PauliEvolution":
            evo = inst.operation
            if isinstance(evo.operator, list):
                raise ValueError("Grouped operators in Pauli not supported.")

            op = evo.operator.to_sparse_list()
            if len(op) > 1:
                raise ValueError("PauliEvolution is not a single rotation.")
            paulis, indices, coeff = op[0]

            basis = ["I"] * pbc.num_qubits
            for pauli, i in zip(paulis, indices):
                basis[i] = pauli

            angle = evo.params[0] * np.real(coeff)

            rot = {"Rotation": {"basis": basis, "angle": str(angle)}}
            yield to_str(rot)

        elif inst.name == "pauli_product_measurement":
            ppm = inst.operation

            # TODO Use a public interface, once available.
            # See also https://github.com/Qiskit/qiskit/issues/15468.
            z, x, phase = ppm._to_pauli_data()

            basis = ["I"] * pbc.num_qubits
            for qubit, zq, xq in zip(inst.qubits, z, x):
                basis[qubit_to_index[qubit]] = PAULI_TABLE[(zq, xq)]

            flipped = bool(phase == 2)
            meas = {"Measurement": {"basis": basis, "flip_result": flipped}}
            yield to_str(meas)

        else:
            raise ValueError(f"Unsupported instruction in PBC circuit: {inst.name}")
