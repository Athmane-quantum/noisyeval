"""Load benchmark tasks from the tasks/ folder."""
import json
from pathlib import Path

REQUIRED_KEYS = {"id", "prompt", "n_qubits", "expected"}


def load_task(path) -> dict:
    with open(path, encoding="utf-8") as f:
        task = json.load(f)
    missing = REQUIRED_KEYS - set(task)
    if missing:
        raise ValueError(f"{path}: missing keys {sorted(missing)}")
    total = sum(task["expected"].values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"{path}: expected probabilities sum to {total}, not 1")
    for outcome in task["expected"]:
        if len(outcome) != task["n_qubits"]:
            raise ValueError(f"{path}: outcome {outcome!r} does not match n_qubits")
    return task


def load_tasks(folder) -> dict:
    tasks = {}
    for path in sorted(Path(folder).glob("*.json")):
        task = load_task(path)
        tasks[task["id"]] = task
    return tasks
