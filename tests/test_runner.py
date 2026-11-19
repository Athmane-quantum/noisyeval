import pytest
from qiskit import QuantumCircuit

from noisyeval.metrics import counts_to_probs, total_variation_distance
from noisyeval.runner import check_circuit, run_on_simulator

BELL_TASK = {"id": "bell", "n_qubits": 2, "expected": {"00": 0.5, "11": 0.5}}


def bell():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def test_correct_bell_circuit_is_close_to_expected_on_simulator():
    counts = run_on_simulator(bell(), shots=4000)
    tvd = total_variation_distance(counts_to_probs(counts), BELL_TASK["expected"])
    assert tvd < 0.05


def test_filter_rejects_wrong_qubit_count():
    with pytest.raises(ValueError):
        check_circuit(QuantumCircuit(3, 3), BELL_TASK)


def test_filter_rejects_circuit_without_measurement():
    qc = QuantumCircuit(2)
    qc.h(0)
    with pytest.raises(ValueError):
        check_circuit(qc, BELL_TASK)
