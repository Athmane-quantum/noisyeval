# model: claude-opus-5-5 | date: 2026-11-17 | prompt: tasks/bb84_x1.json | output saved unedited
from qiskit import QuantumCircuit


def build_circuit():
    qc = QuantumCircuit(1, 1)
    # Alice: bit 1 in the X basis -> |->
    qc.x(0)
    qc.h(0)
    # Bob: measure in the X basis (rotate back with H, then measure in Z)
    qc.h(0)
    qc.measure(0, 0)
    return qc
