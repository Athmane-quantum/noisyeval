# NoisyEval

**Does AI-generated quantum code survive real hardware?**

Benchmarks for AI-written quantum code (Qiskit HumanEval, 2024; Qiskit QuantumKatas, arXiv:2605.27210)
check whether the code is valid or whether its output is right on an ideal, noiseless simulator.
A 2026 review of generative AI for quantum code (Merilehto, arXiv:2603.16216) notes that end-to-end
evaluation on real quantum hardware is missing.

NoisyEval closes that gap on a small scale: each task is given to an AI model, the generated circuit is
run unedited on a simulator and on a real quantum processor, and the result is compared with the
expected distribution, together with its real cost.

## Status

**Prototype (November 2026):** 3 tasks, 1 AI model, ideal simulator + one run on real IBM hardware.

The funded version targets about 20 tasks, 3 AI models with frozen versions, and 3 hardware
technologies (IBM, IQM, Rigetti, plus IonQ on a subset), with the cost per valid result in dollars.

## Tasks

| ID | Task | Expected result |
|---|---|---|
| `bell` | Bell state on 2 qubits, measured | `00`: 50 %, `11`: 50 % |
| `ghz3` | GHZ state on 3 qubits, measured | `000`: 50 %, `111`: 50 % |
| `bb84_x1` | One BB84 round: bit 1 encoded in the X basis, measured in the X basis | `1`: 100 % |

Each task is a JSON file in `tasks/` with the exact prompt given to the model.
Generated code is saved unedited in `generated/<model>/<task>.py`, with the model name and date.

## Metric

**Total variation distance** between the measured and the expected distribution:
for each possible outcome, take the gap between the two probabilities, add the gaps, divide by two.
0 % means a perfect match, 100 % means no outcome in common.

Example: expected `00` 50 %, `11` 50 %; measured `00` 48 %, `11` 47 %, `01` 3 %, `10` 2 %.
Gaps 2 + 3 + 3 + 2 = 10 %, halved: **5 %**.

Before any run, a filter rejects circuits with the wrong number of qubits, no measurement,
or a depth above 50: this protects the hardware budget.

## Results (prototype)

| Model | Task | Code ran | Distance, simulator | Distance, IBM hardware | IBM job ID |
|---|---|---|---|---|---|
| claude-opus-5-5 | bell | yes | 0.6 % | 7.8 % | `dbvf6ohcn7vc73egpn9g` |
| claude-opus-5-5 | ghz3 | yes | 0.4 % | — | — |
| claude-opus-5-5 | bb84_x1 | yes | 0.0 % | — | — |

4,000 shots per run. IBM backend: `ibm_fez` (November 19, 2026). Raw rows in `results/results.csv`.

On the ideal simulator the Bell circuit lands 0.6 % away from the expected distribution; on real IBM hardware the same unedited circuit lands 7.8 % away. That gap is what NoisyEval measures.

## Reproduce

```
pip install -e .[dev]
pytest
python scripts/evaluate.py              # simulator only
python scripts/evaluate.py --ibm bell   # also run 'bell' on IBM hardware (needs a saved IBM account)
```

## Limits

- 3 tasks and 1 model: this prototype shows the pipeline works, not which model is best.
- The generated code comes from a chat session, saved unedited; the funded version calls model APIs
  automatically with frozen versions and published prompts.
- Generated code is executed locally: read it before running it.

## About the author

- First place, Qiskit Fall Fest 2026 Stuttgart (intermediate/advanced track)
- Merged open-source contribution to Qibo: https://github.com/qiboteam/qibo/pull/1905
- BB84 simulator with DOI: https://github.com/Athmane-quantum/bb84-sim

## License

MIT
