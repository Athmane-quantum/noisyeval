# NoisyEval

**Does AI-generated quantum code survive real hardware?**

Existing benchmarks for AI-written quantum code check syntax or ideal-simulator output.
NoisyEval runs the generated circuits on real quantum processors and reports, per task and per model:
whether the code runs, how close the result is to the expected distribution, and the real cost in dollars.

## Status

Prototype (November 2026): 3 tasks, 1 AI model, ideal simulator + IBM Quantum (free plan).

## Tasks

| ID | Task | Expected result |
|---|---|---|
| bell | _to fill_ | _to fill_ |
| ghz3 | _to fill_ | _to fill_ |
| bb84_x1 | _to fill_ | _to fill_ |

## Metric

_to fill: how the distance to the expected distribution is computed, with one numeric example._

## Results

_to fill: table from results/results.csv, with IBM job IDs._

## Reproduce

```
pip install -e .[dev]
pytest
python scripts/evaluate.py
```

## Limits

_to fill: what the prototype does not show yet._

## License

MIT
