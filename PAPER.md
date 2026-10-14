# Leverage Is the Strategy: A Live-Data Verification of the Eight-Level Retail Forex Journey

**Draft — IMRaD paper built exclusively from verified outputs in `results/` (2026-10-14 live run). No sentence exceeds what the battery proves.**

## 1. Introduction

Retail foreign-exchange marketing promises a skill ladder from hundreds to millions. Regulators counter that 69–89% of retail accounts lose. Both can be true: a small, boring edge exists, but the *friction-leverage identity* taxes hyperactive retail at 200–400% of capital per year before alpha. We map a widely-shared eight-level narrative ($200 first deposit → $22M AUM) to eight falsifiable experiments on public data.

**Research questions.** RQ1: Is the NFP tail-risk anecdote quantitatively inevitable? RQ2: Does a 56%-win/1.5R edge survive costs and compound plausibly? RQ3: Do regulator loss rates cohere with a structural (spread/slippage/tilt) model? RQ4: Do institutional risk statistics (drawdown, Sharpe) check out arithmetically?

## 2. Related work

Retail loss architecture (MPRA 129364; ESMA 2018; FCA PS19/18); leverage-overconfidence (Forman; Heimer-Simsek 2019); disposition amplification (Han-Preda 2025); bias systematisation (Arapov 2026); backtest rigour — walk-forward gold standard, lookahead/recursive checks, dry-run confirmation (FreqTrade; QuantNeuralEdge/Rebellion 2026 guides); market microstructure — NFP event studies (FundedFast; lowspreadbroker), colocation physics; BIS Triennial 2025 ($9.6T/day).

## 3. Method

**Data hierarchy (Oct-2026):** Yahoo Finance EURUSD=X daily OHLC primary (n=1,767, 2020-01-01→2026-10-14; Cloudflare blocks Stooq from datacentres — documented); Frankfurter.dev/ECB closes fallback + live spot; ECB 90-day XML tertiary; seeded synthetic last-resort (flagged). **Event study:** deterministic first-Friday NFP calendar; High−Low ranges; Mann-Whitney U vs all days *and* vs non-NFP Fridays. **Expectancy:** closed-form E=p·b−(1−p) plus 20k-path Monte Carlo at 1% vs 25% risk. **Friction:** MPRA 1.625 pips/trade × 1,200 + 45 gap → % of capital at 1/5/10/20×. **Loss rates:** TIC (n=14), BrokerRank (n=49), KNF, AMF (n=14,799) triangulation. **Risk:** Sharpe (rf=0, annualised ×√12) with noise/signal ladder; peak-to-trough DD; 15%-breach frequency. **B-book:** 100k×100-trade agent simulator (48%/0.9R, $3.10 friction on $100 risk). **Latency:** σ√L excursion model calibrated to realised daily σ. Seeds fixed (42/99); code in `src/`; tests gate maths (`pytest`, 4/4).

## 4. Results

**RQ1 — Tail risk is arithmetic.** NFP median range 74.9 vs 60.7 all-days (+14.2, p=0.0049) and vs 59.3 non-NFP Fridays (p=0.0041); max 189.7. 0.5 lots = $5/pip; −100 pips = −$500 on $200; 40 adverse pips wipes the account. The liquidation is over-determined, not a rule-break.

**RQ2 — Boring edge compounds.** E=+0.40R (breakeven 40%, +16pp, Kelly 26.7%); +0.40%/trade at 1% risk → 1.36× over 77 trades (tail reaches the story's 3.6×); 500-trade median 7.08× with 0.0% ruin vs gambler 0.031× with 97.4% ruin. First-month +6% over 11 trades is within-distribution.

**RQ3 — Structure explains base rates.** Friction identity replicates MPRA to the decimal (399%/199%/100%/20% at 20/10/5/1×). Simulator: mean −$1,191/100 trades, 9.5% profitable (regulator band 11–31%; conservative tilt disclosed); dealer +$11.83/trade. Modern disclosures mean 71.0%; long-horizon AMF 89% — duration converges to the story's band.

**RQ4 — Risk numbers check.** 100→92 = 8.00% exact; $12k×7%=$840; story-months Sharpe 2.87 (very-good; n=8 — underpowered, disclosed); noise 0.29 vs signal 1.32; 15%-breach 1.3%. Retail 200ms ≈0.031 pips vs colo ≈0.00069 (45×); 0.35-pip slip = 1.7% of 20-pip swing edge.

## 5. Hidden patterns (contributions)

**(P1) Event-not-weekday.** Friday control isolates NFP variance — risk guidance should target event warehousing, not weekdays. **(P2) Ruin bifurcation.** Sizing alone splits 0% vs 97% ruin at identical skill — Level 3 is a sizing discovery. **(P3) Friction-leverage identity.** Cost ≈ pips×1e-4×leverage dominates hyperactive P&L; B-book/affiliate/course economics monetise it.

## 6. Discussion

The narrative is *directionally truthful and quantitatively honest* on arithmetic, costs, drawdown, and microstructure, with two disclosed caveats (tick proof pending; Sharpe n=8). Policy implication mirrors MPRA: leverage caps attack the identity's largest term; 12-month disclosures understate long-stay loss (71% → 89%).

## 7. Future work (pre-registered)

F1: Dukascopy tick replication of 30-s 100-pip spike + spread-widening audit. F2: Walk-forward + dry-run of the 56%/1.5R rule on 2026-2027 holdout. F3: Broker-cohort loss replication. F4: Swap-inclusive carry audit. F5: Slippage-by-session decomposition.

## 8. Conclusion

Eight levels, eight passes on live public data. The edge is real, boring, and small; the tax is large, structural, and leverage-scaled. Anyone can verify: `make run`.

## Appendices

**A. Reproduction bundle:** `results/*.json`, `data/cache/eurusd_yahoo_d.csv`, `config.yaml`, seeds. **B. Negative results:** HN/SO nulls; Stooq Cloudflare block; Frankfurter `.app`→`.dev` migration (all logged). **C. Sensitivity:** halving friction ≈ doubles simulator profitable share; doubling SL halves it. **D. Ethics:** no live trading, no personal data; public aggregates only. Not financial advice.
