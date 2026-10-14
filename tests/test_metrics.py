import sys
sys.path.insert(0, "src")
from metrics import (
    pip_value_usd_simple, pnl_for_pips, expectancy_per_trade,
    required_winrate, max_drawdown, sharpe_ratio, margin_liquidation_move_pips,
)
import numpy as np

def test_pip_math():
    assert pip_value_usd_simple(0.5) == 5.0
    assert pnl_for_pips(-100, 0.5) == -500.0
    assert margin_liquidation_move_pips(200, 0.5) == 40.0

def test_expectancy():
    assert abs(expectancy_per_trade(0.56, 1.5) - 0.40) < 1e-9
    assert abs(required_winrate(1.5) - 0.4) < 1e-9

def test_drawdown():
    eq = np.array([100.0, 110, 105, 92])
    dd = max_drawdown(eq)
    assert abs(dd - (110 - 92) / 110) < 1e-9

def test_sharpe_zero():
    assert sharpe_ratio(np.array([0.01, 0.01, 0.01])) == 0.0
