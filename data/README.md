# data/

- `cache/eurusd_yahoo_d.csv` — live Yahoo Finance EURUSD=X daily OHLC (1,767 rows, 2020→2026-10-14). Refresh with `make run` (deletes force re-pull).
- No credentials, no keys, no personal data. Public aggregates only.
- If fully offline the battery uses a seeded synthetic fallback flagged `_synthetic_fallback` (never presented as live).
