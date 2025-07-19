


import random
import pytest

from your_module import simulate_monty_hall

def test_simulate_monty_hall_stay_reproducible():
    random.seed(123)
    wins = simulate_monty_hall(trials=1000, strategy="stay")
    win_rate = wins / 1000
    # Theoretical win rate for “stay” is ~1/3
    assert abs(win_rate - (1/3)) < 0.05

def test_simulate_monty_hall_switch_reproducible():
    random.seed(123)
    wins = simulate_monty_hall(trials=1000, strategy="switch")
    win_rate = wins / 1000
    # Theoretical win rate for “switch” is ~2/3
    assert abs(win_rate - (2/3)) < 0.05

def test_simulate_monty_hall_zero_trials():
    with pytest.raises(ValueError):
        simulate_monty_hall(trials=0, strategy="switch")

def test_simulate_monty_hall_invalid_strategy():
    with pytest.raises(ValueError):
        simulate_monty_hall(trials=100, strategy="random_choice")
