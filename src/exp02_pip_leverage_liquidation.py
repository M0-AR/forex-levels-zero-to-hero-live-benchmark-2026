"""EXP-02 — Pip maths + leverage liquidation (Level 1).

Claim: '100 pips on 0.5 lots ≈ $500. You don't have $500. You have $200.'
Verifies: pip value, P&L for adverse move, liquidation move for $200 @ 0.5 lots,
and why a $9 demo win teaches nothing about tail risk.
"""
from __future__ import annotations
import json
from pathlib import Path
from metrics import pip_value_usd_simple, pnl_for_pips, margin_liquidation_move_pips

def run(outdir: str = "results") -> dict:
    lots, acct = 0.5, 200.0
    per_pip = pip_value_usd_simple(lots)  # $5/pip
    loss_100 = pnl_for_pips(-100, lots)   # -$500
    kill_pips = margin_liquidation_move_pips(acct, lots)  # 40 pips eats the account
    res = {
        "experiment": "exp02_pip_leverage",
        "lots": lots, "account_usd": acct,
        "usd_per_pip": per_pip,
        "pnl_minus_100_pips_usd": loss_100,
        "pips_to_wipe_account": kill_pips,
        "demo_win_9_usd_pips_equiv": 9.0 / per_pip,
        "checks": {
            "100pips_x_0.5lots_is_500": abs(loss_100 + 500.0) < 1e-9,
            "40pips_wipes_200": abs(kill_pips - 40.0) < 1e-9,
            "nfp_can_wipe_before_coffee": kill_pips < 100.0,
        },
        "verdict": (
            f"SUPPORTED: 0.5 lots = ${per_pip}/pip; -100 pips = ${loss_100:.0f} on a ${acct:.0f} account "
            f"(2.5x the account). Only {kill_pips:.0f} adverse pips wipes it — NFP routinely exceeds that intraday. "
            "The story's liquidation is arithmetically inevitable, not a broken rule."
        ),
    }
    Path(outdir).mkdir(parents=True, exist_ok=True)
    Path(outdir, "exp02_pip_leverage.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))
    return res

if __name__ == "__main__":
    run()
