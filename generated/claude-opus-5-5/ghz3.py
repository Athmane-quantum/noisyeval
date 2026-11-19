# model: claude-opus-5-5 | date: 2026-11-17 | prompt: tasks/ghz3.json | output saved unedited
from qiskit import QuantumCircuit


def build_circuit():
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure(range(3), range(3))
    return qc
