from pathlib import Path

from noisyeval.tasks import load_tasks

TASKS = Path(__file__).resolve().parent.parent / "tasks"


def test_all_tasks_load_and_are_consistent():
    tasks = load_tasks(TASKS)
    assert set(tasks) == {"bell", "ghz3", "bb84_x1"}
    for task in tasks.values():
        assert sum(task["expected"].values()) == 1
        assert all(len(o) == task["n_qubits"] for o in task["expected"])
