from ftcc.compilation_layers.qiskit_layer import QiskitBicycleLayer
from ftcc.compilation_layers.nwqec_layer import NWQECPauliLayer

import json


def translate_nwqec_to_qiskit_bicycle(nwqec_layer: NWQECPauliLayer):
    metadata = nwqec_layer.metadata
    circuit = nwqec_layer.circuit.to_qasm_str()

    pbc_dict_iter = get_dict_entry_iter(circuit)

    json_circuit = "\n".join(map(json.dumps, pbc_dict_iter))

    bicycle_layer = QiskitBicycleLayer(json_circuit, metadata)

    return bicycle_layer


def get_dict_entry_iter(circuit):
    for instruction in circuit.split("\n")[5:-1]:
        print("INSTRUCTION: ", instruction)
        inst_name, pauli_str = instruction.split(" ")
        if inst_name == "m_pauli":
            flipped = True if pauli_str[0] == "-" else False
            basis = [char for char in pauli_str[1:-1]]
            yield {"Measurement": {"basis": basis, "flip_result": flipped}}
        else:
            print(f"{inst_name} is not a Pauli measurement!")
            raise NotImplementedError
