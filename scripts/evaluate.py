"""Run every generated circuit on the simulator (and optionally one task on IBM).

Usage:
    python scripts/evaluate.py                 # simulator only
    python scripts/evaluate.py --ibm bell      # also run task 'bell' on IBM hardware
"""
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

from noisyeval.metrics import counts_to_probs, total_variation_distance
from noisyeval.runner import check_circuit, load_generated_circuit, run_on_ibm, run_on_simulator
from noisyeval.tasks import load_tasks

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["timestamp", "task", "model", "ran_ok", "error", "shots",
          "sim_tvd", "hw_backend", "hw_tvd", "hw_job_id"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ibm", metavar="TASK_ID", help="also run this task on IBM hardware")
    parser.add_argument("--shots", type=int, default=4000)
    args = parser.parse_args()

    tasks = load_tasks(ROOT / "tasks")
    rows = []
    for model_dir in sorted(p for p in (ROOT / "generated").iterdir() if p.is_dir()):
        for task_id, task in tasks.items():
            path = model_dir / f"{task_id}.py"
            if not path.exists():
                continue
            row = {f: "" for f in FIELDS}
            row.update(timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                       task=task_id, model=model_dir.name, shots=args.shots)
            try:
                circuit = load_generated_circuit(path)
                check_circuit(circuit, task)
                sim_counts = run_on_simulator(circuit, shots=args.shots)
                row["sim_tvd"] = round(total_variation_distance(
                    counts_to_probs(sim_counts), task["expected"]), 4)
                if args.ibm == task_id:
                    hw_counts, job_id, backend = run_on_ibm(circuit, shots=args.shots)
                    row["hw_tvd"] = round(total_variation_distance(
                        counts_to_probs(hw_counts), task["expected"]), 4)
                    row["hw_job_id"], row["hw_backend"] = job_id, backend
                row["ran_ok"] = True
            except Exception as exc:  # a broken generated circuit is a result, not a crash
                row["ran_ok"], row["error"] = False, f"{type(exc).__name__}: {exc}"
            rows.append(row)
            print(f"{row['model']:>18} {task_id:>8}  ok={row['ran_ok']}  "
                  f"sim_tvd={row['sim_tvd']}  hw_tvd={row['hw_tvd']}  {row['error']}")

    out = ROOT / "results" / "results.csv"
    new_file = not out.exists()
    with open(out, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerows(rows)
    print(f"\n{len(rows)} rows appended to {out}")


if __name__ == "__main__":
    main()
