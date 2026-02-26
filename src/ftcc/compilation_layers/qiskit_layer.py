from ftcc.compilation_layers.base_layer import BaseLayer

import qiskit
from qiskit.transpiler.passes import LitinskiTransformation
import os
import subprocess


class QiskitPBCLayer(BaseLayer):
    def __init__(self, circuit, metadata):
        self.metadata = metadata
        self.circuit = circuit

    def compile(self, fix_clifford=True):
        lit = LitinskiTransformation(fix_clifford=fix_clifford)
        self.circuit = lit(self.circuit)

        return


class QiskitBicycleLayer(BaseLayer):
    """
    This layer implements the Bicycle Architecture outlined in the Tour de Gross paper,
    largely based on code from the bicycle-architecture-compiler qiskit-community repo.
    Assumes that metadata defines a codename and that circuit is a PBC circuit in the
    dict IR used by the compiler. Also assumes that rust is installed and PyGridSynth
    is in the current venv, though the latter is not imported (it is used by
    bicycle_compiler).
    """

    def __init__(self, circuit, metadata):
        self.metadata = metadata
        self.circuit = circuit

    def compile(self):
        # compile the rust binaries if they do not exist
        rust_binary_path = f"{os.getcwd()}/build_rust"
        if not os.path.exists(rust_binary_path):
            self.__compile_rust_binaries__(rust_binary_path)

        # generate measurement tables if they do not yet exist
        codename = self.metadata["code_name"]
        measurement_table_path = f"measurement_tables/table_{codename}.dat"
        if not os.path.exists(measurement_table_path):
            self.__generate_measurement_table__(codename, measurement_table_path)

        # compile the pbc circuit
        self.circuit = self.__run_command__(
            f"{rust_binary_path}/bin/bicycle_compiler",
            codename,
            "--measurement-table",
            measurement_table_path,
            input_data=self.circuit,
        )

        return

    def __compile_rust_binaries__(self, filepath):
        subprocess.run(["cargo", "install", "bicycle_compiler", "--root", filepath])
        return

    def __generate_measurement_table__(self, codename, filepath):
        # rust_binary_path = f"{os.getcwd()}/build_rust"
        self.__run_command__(
            f"{os.getcwd()}/build_rust/bin/bicycle_compiler",
            f"{codename}",
            "generate",
            filepath,
        )

    def __run_command__(self, *cmdlist: list[str], input_data=None):
        """process = await asyncio.create_subprocess_exec(
            *[str(x) for x in cmdlist],
            stdin=asyncio.subprocess.PIPE if input_data is not None else None,
            stdout=asyncio.subprocess.PIPE,
            stderr==asyncio.subprocess.PIPE
        )"""
        completed_proc = subprocess.run(
            [str(x) for x in cmdlist],
            input=input_data.encode("utf-8") if input_data is not None else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        """stdout, stderr = await process.communicate(
            input=input_data.encode('utf-8') if input_data is not None else None
        )"""
        stdout = completed_proc.stdout
        stderr = completed_proc.stderr
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")
        return stdout.decode()
