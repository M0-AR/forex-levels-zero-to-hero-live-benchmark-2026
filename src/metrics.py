"""Shared risk/performance mathematics. All pure functions, unit-tested."""

from __future__ import annotations

import numpy as np


def pip_value_usd(lots: float, eurusd: float = 1.10) -> float:
    """USD per pip for EUR/USD long.

    1 standard lot = 100_000 EUR. 1 pip = 0.0001 price units.
    value_in_quote_USD = lots * 100_000 * 0.0001 / eurusd * eurusd...
    Simplification used across retail docs: ~$10/pip/lot at 1.10,
    scaled linearly. We keep the scaling explicit so the $500/100-pip
    claim is auditable.
    """
    return lots * 100_000 * 0.0001
    # == lots * 10.0 USD per pip (1 standard lot = $10/pip on EUR/USD)


def pip_value_usd_simple(lots: float) -> float:
    return lots * 10.0


def pnl_for_pips(pips: float, lots: float) -> float:
    return pips * pip_value_usd_simple(lots)


def expectancy_per_trade(winrate: float, avg_win_R: float, avg_loss_R: float = 1.0) -> float:
    """Expectancy in units of R (risk units)."""
    return winrate * avg_win_R - (1.0 - winrate) * avg_loss_R


def required_winrate(rr: float) -> float:
    """Breakeven win rate for a given reward:risk ratio."""
    return 1.0 / (1.0 + rr)


def max_drawdown(equity: np.ndarray) -> float:
    """Max drawdown as fraction (0..1)."""
    equity = np.asarray(equity, dtype=float)
    peak = np.maximum.accumulate(equity)
    dd = (peak - equity) / np.maximum(peak, 1e-12)
    return float(np.max(dd))


def sharpe_ratio(returns: np.ndarray, periods_per_year: int = 12) -> float:
    """Annualised Sharpe (risk-free = 0). Returns are per-period simple returns."""
    r = np.asarray(returns, dtype=float)
    if r.size < 3 or float(np.std(r, ddof=1)) == 0:
        return 0.0
    return float(np.mean(r) / np.std(r, ddof=1) * np.sqrt(periods_per_year))


def margin_liquidation_move_pips(account_usd: float, lots: float, stopout_frac: float = 0.5) -> float:
    """Adverse pip move that wipes usable margin to stop-out.

    Retail stop-out ~50% of margin (FCA/ESMA). For a pure loss estimate
    we report the move that consumes the whole account:
        pips = account / ($/pip).
    """
    per_pip = pip_value_usd_simple(lots)
    return account_usd / per_pip if per_pip > 0 else float("inf")


def kelly_fraction(winrate: float, rr: float) -> float:
    """Kelly fraction of bankroll for binary R-multiple bets: f* = p - (1-p)/b."""
    return winrate - (1.0 - winrate) / rr if rr > 0 else 0.0
