"""Live + cached public FX data. No API keys. Fully offline-capable."""

from __future__ import annotations

import calendar
import datetime as dt
import os
from pathlib import Path

import pandas as pd
import requests

STOOQ_DAILY = "https://stooq.com/q/d/l/?s=eurusd&i=d"
FRANKFURTER = "https://api.frankfurter.dev/v1"
YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/EURUSD=X"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) forex-benchmark/1.0"}


def _cache(path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _synthetic_daily() -> pd.DataFrame:
    import numpy as np
    rng = np.random.default_rng(42)
    dates = pd.date_range("2020-01-01", "2026-10-01", freq="B")
    rets = rng.normal(0.0001, 0.0045, len(dates))
    price = 1.10 * (1 + rets).cumprod()
    df = pd.DataFrame({
        "Date": dates,
        "Open": price * (1 - 0.0005),
        "High": price * (1 + abs(rng.normal(0, 0.002, len(dates)))),
        "Low": price * (1 - abs(rng.normal(0, 0.002, len(dates)))),
        "Close": price,
        "Volume": 0,
    })
    df["_synthetic_fallback"] = True  # type: ignore
    return df


def fetch_yahoo_daily(cache: str = "data/cache/eurusd_yahoo_d.csv", timeout: int = 30) -> pd.DataFrame | None:
    """Yahoo Finance EURUSD=X daily OHLC. Returns None if unreachable."""
    import time
    cp = _cache(cache)
    # 2020-01-01 → now
    p1 = int(dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc).timestamp())
    p2 = int(time.time())
    url = f"{YAHOO_CHART}?interval=1d&period1={p1}&period2={p2}"
    r = requests.get(url, timeout=timeout, headers=UA)
    r.raise_for_status()
    j = r.json()
    res = j["chart"]["result"][0]
    ts = res["timestamp"]
    q = res["indicators"]["quote"][0]
    df = pd.DataFrame({
        "Date": pd.to_datetime(ts, unit="s").tz_localize("UTC").tz_convert(None),
        "Open": q["open"], "High": q["high"], "Low": q["low"],
        "Close": q["close"], "Volume": q.get("volume", [0] * len(ts)),
    }).dropna(subset=["Close"])
    df.to_csv(cp, index=False)
    return df


def fetch_frankfurter_history(start: str = "2020-01-01", timeout: int = 30) -> pd.DataFrame | None:
    """Frankfurter/ECB daily closes (no H/L). Returns None if unreachable."""
    import datetime as _dt
    end = _dt.date.today().isoformat()
    url = f"{FRANKFURTER}/{start}..{end}?from=EUR&to=USD"
    r = requests.get(url, timeout=timeout, headers=UA)
    r.raise_for_status()
    rates = r.json().get("rates", {})
    rows = [(d, v["USD"]) for d, v in sorted(rates.items())]
    if not rows:
        return None
    df = pd.DataFrame(rows, columns=["Date", "Close"])
    df["Date"] = pd.to_datetime(df["Date"])
    for c in ("Open", "High", "Low"):
        df[c] = df["Close"]
    df["Volume"] = 0
    return df


def fetch_stooq_daily(cache: str = "data/cache/eurusd_stooq_d.csv", timeout: int = 30) -> pd.DataFrame:
    """Primary: Yahoo OHLC → fallback Frankfurter closes → fallback cache → synthetic.

    (Oct-2026: Stooq is behind a Cloudflare JS challenge from datacentres, so the
    2026 best-practice primary is Yahoo Finance OHLC; Stooq URL retained for
    desktop/browser use. Function name kept for API stability.)
    """
    # 1) fresh cache less than 24h old with real OHLC columns?
    for fn in ("data/cache/eurusd_yahoo_d.csv", cache):
        cp = Path(fn)
        if cp.exists() and cp.stat().st_size > 1000:
            try:
                df = pd.read_csv(cp, parse_dates=["Date"])
                if set(("Open", "High", "Low", "Close")).issubset(df.columns) and len(df) > 500:
                    import time as _t
                    if _t.time() - cp.stat().st_mtime < 86400:
                        df = df.sort_values("Date").reset_index(drop=True)
                        df["range_pips"] = (df["High"] - df["Low"]) / 0.0001
                        df["body_pips"] = (df["Close"] - df["Open"]).abs() / 0.0001
                        df["_stale_cache"] = True  # type: ignore
                        return df
            except Exception:
                pass
    # 2) live Yahoo
    try:
        df = fetch_yahoo_daily()
        assert df is not None and len(df) > 500
    except Exception as e1:
        print(f"[data_loader] Yahoo failed ({e1}), trying Frankfurter/ECB…")
        try:
            df = fetch_frankfurter_history()
            assert df is not None and len(df) > 500
            df["_frankfurter_close_only"] = True  # type: ignore
        except Exception as e2:
            cands = [Path("data/cache/eurusd_yahoo_d.csv"), _cache(cache)]
            for cp in cands:
                if cp.exists() and cp.stat().st_size > 1000:
                    try:
                        df = pd.read_csv(cp, parse_dates=["Date"])
                        break
                    except Exception:
                        continue
            else:
                print(f"[data_loader] WARN offline, synthetic fallback used ({e2})")
                df = _synthetic_daily()
    df = df.sort_values("Date").reset_index(drop=True)
    df["range_pips"] = (df["High"] - df["Low"]) / 0.0001
    df["body_pips"] = (df["Close"] - df["Open"]).abs() / 0.0001
    return df


def first_fridays(start: str = "2020-01-01", end: str = "2026-10-01") -> list[dt.date]:
    """First Friday of each month — the NFP release date rule (8:30am ET)."""
    s = dt.date.fromisoformat(start)
    e = dt.date.fromisoformat(end)
    out: list[dt.date] = []
    y, m = s.year, s.month
    while (y, m) <= (e.year, e.month):
        # first Friday
        c = calendar.monthcalendar(y, m)
        # Friday = index 4
        fri = c[0][4] or c[1][4]
        d = dt.date(y, m, fri)
        if s <= d <= e:
            out.append(d)
        m += 1
        if m == 13:
            m, y = 1, y + 1
    return out


def fetch_frankfurter_latest(base: str = "USD", symbols: str = "EUR,GBP,JPY", timeout: int = 20) -> dict:
    """Live spot check (ECB via Frankfurter). Returns dict with rates + date."""
    for host in (FRANKFURTER, "https://api.frankfurter.app/v1"):
        try:
            url = f"{host}/latest?from={base}&to={symbols}"
            r = requests.get(url, timeout=timeout, headers=UA)
            r.raise_for_status()
            return r.json()
        except Exception:
            continue
    # last resort: open.er-api.com (free, no key)
    r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=timeout, headers=UA)
    r.raise_for_status()
    j = r.json()
    return {"base": "USD", "date": j.get("time_last_update_utc"), "rates": {k: j["rates"][k] for k in ("EUR", "GBP", "JPY")}}
