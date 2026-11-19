import pytest

from noisyeval.metrics import counts_to_probs, total_variation_distance


def test_identical_distributions_have_zero_distance():
    p = {"00": 0.5, "11": 0.5}
    assert total_variation_distance(p, p) == 0


def test_disjoint_distributions_have_distance_one():
    assert total_variation_distance({"00": 1.0}, {"11": 1.0}) == 1


def test_hand_computed_example():
    # expected 50/50 on 00 and 11; measured 48, 47, 3, 2 percent
    # gaps: 2 + 3 + 3 + 2 = 10 percent, halved -> 5 percent
    expected = {"00": 0.5, "11": 0.5}
    measured = {"00": 0.48, "11": 0.47, "01": 0.03, "10": 0.02}
    assert total_variation_distance(expected, measured) == pytest.approx(0.05)


def test_counts_to_probs_normalises_and_strips_spaces():
    probs = counts_to_probs({"0 0": 30, "11": 70})
    assert probs == pytest.approx({"00": 0.3, "11": 0.7})


def test_counts_to_probs_rejects_empty_counts():
    with pytest.raises(ValueError):
        counts_to_probs({})
