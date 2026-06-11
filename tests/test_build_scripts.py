import pytest
import tomllib

from ftcc.get_requirements import get_requirements
from ftcc import Pipeline

from qiskit import QuantumCircuit as QiskitCircuit

"""from ftcc.compilation_layers import (
    QiskitPBCLayer,
    QiskitBicycleLayer,
    MQTEncodingLayer,
    TopologiqLayer,
    TQECLayer,
    PyZXLayer,
    BaseLayer,
)"""


def test_build_info_correctness():
    filename = "src/ftcc/_build_info.toml"

    with open(filename, "rb") as f:
        build_info = tomllib.load(f)

    print(build_info["dependency-groups"])
    print(build_info["dependency-conflicts"])
    print(build_info["dependency-sources"])


def test_requirements_build_script():
    path = ["QiskitPBCLayer", "QiskitBicycleLayer"]
    get_requirements(path)


def test_full_pipeline():
    qc = QiskitCircuit(4, 4)
    qc.t(0)
    qc.cx(2, 1)
    qc.sxdg(3)
    qc.cx(1, 0)
    qc.sx(2)
    qc.t(3)
    qc.cx(3, 0)
    qc.t(0)
    qc.s(1)
    qc.t(2)
    qc.s(3)
    qc.sxdg(0)
    qc.sx(1)
    qc.sx(2)
    qc.sx(3)
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.measure(2, 2)
    qc.measure(3, 3)

    pipeline = Pipeline(qc)
    compilation_path = ["QiskitPBCLayer", "QiskitBicycleLayer"]

    # get path and compile
    pipeline.compile(compilation_path)
