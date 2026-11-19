"""Distances between measurement distributions."""


def counts_to_probs(counts: dict) -> dict:
    """Turn raw counts like {"00": 480, "11": 520} into probabilities.

    Keys are cleaned: spaces that Qiskit inserts between classical
    registers are removed, so "0 1" and "01" are treated the same.
    """
    total = sum(counts.values())
    if total == 0:
        raise ValueError("counts are empty")
    probs = {}
    for outcome, n in counts.items():
        key = outcome.replace(" ", "")
        probs[key] = probs.get(key, 0) + n / total
    return probs


def total_variation_distance(p: dict, q: dict) -> float:
    """Total variation distance between two distributions.

    For every possible outcome, take the gap between the two
    probabilities, add all gaps together, then divide by two.
    0 means identical, 1 means no outcome in common.
    """
    outcomes = set(p) | set(q)
    gaps = [abs(p.get(o, 0.0) - q.get(o, 0.0)) for o in outcomes]
    return sum(gaps) / 2
