"""Load AI-generated circuits, filter them, and run them."""
import importlib.util

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

MAX_DEPTH = 50  # pre-submission filter: protects the hardware budget


def load_generated_circuit(path) -> QuantumCircuit:
    """Import a generated .py file and call its build_circuit() function.

    Generated code comes from an AI model: read it before running it.
    """
    spec = importlib.util.spec_from_file_location("generated_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "build_circuit"):
        raise AttributeError("no build_circuit() function in generated code")
    circuit = module.build_circuit()
    if not isinstance(circuit, QuantumCircuit):
        raise TypeError("build_circuit() did not return a QuantumCircuit")
    return circuit


def check_circuit(circuit: QuantumCircuit, task: dict) -> None:
    """Refuse circuits that break the task contract before spending shots."""
    if circuit.num_qubits != task["n_qubits"]:
        raise ValueError(
            f"circuit has {circuit.num_qubits} qubits, task expects {task['n_qubits']}"
        )
    if circuit.depth() > MAX_DEPTH:
        raise ValueError(f"circuit depth {circuit.depth()} exceeds {MAX_DEPTH}")
    if circuit.count_ops().get("measure", 0) == 0:
        raise ValueError("circuit has no measurement")


def run_on_simulator(circuit: QuantumCircuit, shots: int = 4000, seed: int = 1234) -> dict:
    backend = AerSimulator(seed_simulator=seed)
    compiled = transpile(circuit, backend, seed_transpiler=seed)
    return backend.run(compiled, shots=shots).result().get_counts()


def run_on_ibm(circuit: QuantumCircuit, shots: int = 4000, backend_name=None):
    """Run on a real IBM device (free Open Plan). Returns (counts, job_id, backend_name).

    Needs an account saved once with QiskitRuntimeService.save_account(...).
    """
    from qiskit.transpiler import generate_preset_pass_manager
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

    service = QiskitRuntimeService()
    if backend_name:
        backend = service.backend(backend_name)
    else:
        backend = service.least_busy(operational=True, simulator=False)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)
    sampler = SamplerV2(mode=backend)
    job = sampler.run([isa_circuit], shots=shots)
    pub_result = job.result()[0]
    counts = pub_result.join_data().get_counts()
    return counts, job.job_id(), backend.name
