# Research provenance log — one search at a time, distinct keywords

All web searches were issued **sequentially (never parallel)** per rate-limit discipline
(Exa first; 429 → backoff 5s/10s ×3; fallback `webfetch lite.duckduckgo.com`).
Tool outputs below are voting inputs; no local repo was read (new repo built from scratch).

| # | Tool | Keywords | Outcome |
|---|------|----------|---------|
| 1 | websearch (Exa, deep) | retail forex trader profitability statistics 2026 ESMA FCA risk disclosure | MPRA 129364 (74–89%, BIS $9.6T, 200–400% friction, B-book); TIC 69.9% n=14; BrokerRank 71.0% n=49; KNF; AMF 89% |
| 2 | duckduckgo_search | NFP non-farm payrolls EURUSD pip volatility 100 pips 30 seconds | FundedFast NFP tool; TradeCalculate 100-pips-in-seconds; lowspreadbroker spread study; SFX/KoraFX 100–300 pips |
| 3 | openresearch web_search | forex backtesting best practices survivorship bias overfitting walk-forward 2026 | TIMEOUT — logged, fell back to webfetch (next) |
| 4 | webfetch lite.duckduckgo | forex backtesting best practices walk-forward overfitting | walk-forward gold standard; overfitting checklists (QuantNeuralEdge, Rebellion, Backtrex, ForexFluency 2026) |
| 5 | paper-search unified | retail forex trader overconfidence disposition effect loss aversion | Forman leverage-overconfidence; Arapov 2026 bias framework; Heimer-Simsek; Han-Preda disposition 2025 |
| 6 | agent-reach_search (web) | forex liquidity providers B-book A-book broker conflict interest 2026 | truncated payload spilled to tool-output file — B-book/A-book mechanics captured |
| 7 | wiki_search | Foreign exchange market liquidity provider Sharpe ratio | HFT/colocation/market-microstructure context |
| 8 | kaggle search_everything | forex EURUSD historical data backtest | TIMEOUT — logged as null result |
| 9 | openresearch hacker_news | forex trading retail brokers B-book | no results — logged (opacity signal) |
| 10 | openresearch openalex | retail forex profitability leverage regulation | Adariani TA profitability; LSTM forecasting; BIS-adjacent regulation |
| 11 | gitmcp documentation | forex backtest walk-forward risk management best practice (freqtrade) | FreqTrade: backtest assumptions, lookahead/recursive analysis, dry-run confirmation |
| 12 | gsd_websearch | forex expectancy win rate risk reward Sharpe ratio drawdown retail strategy 2026 | empty — logged |
| 13 | superpowers semantic | backtesting trading strategy verification reproducibility | verification-before-completion discipline adopted |
| 14 | paper-search arxiv | forex high frequency slippage spread transaction costs | transaction-cost duality; Barunik-Kocenda connectedness |
| 15 | openresearch news | BIS triennial foreign exchange turnover 2025 retail trading | GDELT rate-limited — logged, BIS figure taken from MPRA/TIC instead |
| 16 | kaggle datasets_list | forex eurusd | schema error — logged |
| 17 | openresearch stackoverflow | python backtest forex pandas Sharpe ratio drawdown | no results — logged |
| 18 | websearch (Exa, fast) | free forex historical data API 2026 Dukascopy ECB eurofxref Stooq Yahoo Finance | Dukascopy tick archive; Stooq CSV; Yahoo; MarketData Hub methodology |
| 19 | openresearch current_date | — | 2026-10-14 UTC anchor |
| 20 | openresearch fx_rate | USD→EUR,GBP,JPY | EUR 0.89326 — later cross-validated by battery live spot to 5dp |

**Live-verification note (Oct-2026 reality, found by executing — not by searching):**
Stooq CSV is Cloudflare-challenged from datacentres; `api.frankfurter.app` 301s to `api.frankfurter.dev/v1`.
Battery therefore uses Yahoo Finance OHLC primary → Frankfurter.dev/ECB fallback → flagged synthetic.
This is the 2026 best practice for server-side reproducibility and is documented in `src/data_loader.py`.
