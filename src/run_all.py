"""Run the full zero-to-hero verification battery. Writes results/*.json + SUMMARY.md."""
from __future__ import annotations
import argparse, json, traceback
from pathlib import Path

import exp01_nfp_volatility as e01
import exp02_pip_leverage_liquidation as e02
import exp03_expectancy_montecarlo as e03
import exp04_friction_costs as e04
import exp05_loss_rate_benchmark as e05
import exp06_sharpe_drawdown as e06
import exp07_bbook_aggregate as e07
import exp08_slippage_latency as e08
from data_loader import fetch_frankfurter_latest

EXPS = [
    ("EXP-01 NFP volatility", e01.run),
    ("EXP-02 Pip/leverage liquidation", e02.run),
    ("EXP-03 Expectancy Monte Carlo", e03.run),
    ("EXP-04 Friction audit", e04.run),
    ("EXP-05 Loss-rate benchmark", e05.run),
    ("EXP-06 Sharpe/drawdown", e06.run),
    ("EXP-07 B-book aggregate", e07.run),
    ("EXP-08 Slippage/latency", e08.run),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--outdir", default="results")
    args = ap.parse_args()
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    summary_lines = ["# Verification battery — run log", ""]
    results = {}
    for name, fn in EXPS:
        try:
            r = fn(str(outdir))
            results[name] = {"status": "OK", "verdict": r.get("verdict", "")[:400]}
            summary_lines.append(f"- [x] {name}: OK")
        except Exception as e:
            results[name] = {"status": "FAIL", "error": str(e)}
            summary_lines.append(f"- [ ] {name}: FAIL — {e}")
            traceback.print_exc()
    # Live spot check
    try:
        live = fetch_frankfurter_latest()
        results["LIVE_FX_SPOT"] = {"status": "OK", "data": live}
        summary_lines.append(f"- [x] LIVE spot (Frankfurter/ECB): {live}")
    except Exception as e:
        results["LIVE_FX_SPOT"] = {"status": "OFFLINE", "error": str(e)}
        summary_lines.append(f"- [ ] LIVE spot OFFLINE: {e}")
    (outdir / "battery.json").write_text(json.dumps(results, indent=2))
    (outdir / "SUMMARY.md").write_text("\n".join(summary_lines) + "\n")
    print("\n".join(summary_lines))

if __name__ == "__main__":
    main()
