# model: claude-opus-5-5 | date: 2026-11-17 | prompt: tasks/bell.json | output saved unedited
from qiskit import QuantumCircuit


def build_circuit():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc
