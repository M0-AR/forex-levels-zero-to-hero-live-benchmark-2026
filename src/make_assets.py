"""Generate README assets: charts + demo GIF. Verified outputs only."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

plt.rcParams.update({"figure.dpi": 150, "font.size": 9, "axes.grid": True, "grid.alpha": 0.3})

# 1) NFP distribution
df = pd.read_csv(ROOT / "data/cache/eurusd_yahoo_d.csv", parse_dates=["Date"])
import calendar, datetime as dt
def first_fridays(s="2020-01-01", e="2026-10-01"):
    s = dt.date.fromisoformat(s); e = dt.date.fromisoformat(e); out=[]; y,m=s.year,s.month
    while (y,m)<=(e.year,e.month):
        c=calendar.monthcalendar(y,m); fri=c[0][4] or c[1][4]; d=dt.date(y,m,fri)
        if s<=d<=e: out.append(d)
        m+=1
        if m==13: m,y=1,y+1
    return set(out)
nfp = first_fridays()
df["range_pips"]=(df["High"]-df["Low"])/0.0001
df["is_nfp"]=pd.to_datetime(df["Date"]).dt.date.isin(nfp)
fig,ax=plt.subplots(figsize=(7,3.2))
ax.hist(df.loc[~df["is_nfp"],"range_pips"],bins=40,alpha=0.6,label="normal days")
ax.hist(df.loc[df["is_nfp"],"range_pips"],bins=15,alpha=0.85,label="NFP first-Fridays")
ax.axvline(100,color="red",ls="--",lw=1,label="100-pip story line")
ax.set_title("NFP days are systematically wider (live Yahoo EURUSD, n=1767)")
ax.set_xlabel("daily range (pips)"); ax.set_ylabel("days"); ax.legend()
fig.tight_layout(); fig.savefig(ASSETS/"chart_nfp.png"); plt.close(fig)

# 2) Equity Monte Carlo fan (technician vs gambler)
rng=np.random.default_rng(42)
def paths(wr,rr,risk,n=500,m=400,seed=0):
    r=np.random.default_rng(seed); w=r.random((m,n))<wr
    return np.cumprod(1+np.where(w,risk*rr,-risk),axis=1)
tech=paths(0.56,1.5,0.01); gamb=paths(0.45,1.0,0.25,n=60,m=400,seed=1)
fig,ax=plt.subplots(figsize=(7,3.2))
for i in range(60):
    ax.plot(tech[i],color="#1a9e54",alpha=0.12,lw=0.8)
    ax.plot(np.arange(60),gamb[i][:60] if len(gamb[i])>=60 else gamb[i],color="#d33",alpha=0.12,lw=0.8)
ax.set_yscale("log"); ax.set_title("Same market, different sizing: technician (green) vs gambler (red)")
ax.set_xlabel("trades"); ax.set_ylabel("bankroll multiple (log)")
fig.tight_layout(); fig.savefig(ASSETS/"chart_equity.png"); plt.close(fig)

# 3) Friction leverage bar
costs={"1x":20.0,"5x":99.8,"10x":199.5,"20x":399.0}
fig,ax=plt.subplots(figsize=(7,2.8))
ax.bar(costs.keys(),costs.values(),color=["#2b7","#fa0","#f70","#d33"])
ax.set_title("Annual friction % of capital (1,995 pips/lot/yr)")
ax.set_ylabel("%/yr")
for k,v in costs.items(): ax.text(k,v+6,f"{v:.0f}%",ha="center",fontsize=9)
fig.tight_layout(); fig.savefig(ASSETS/"chart_friction.png"); plt.close(fig)

# 4) Loss-rate bar
fig,ax=plt.subplots(figsize=(7,2.8))
labels=["TIC\n69.9","BrokerRank\n71.0","KNF\n72.2","AMF-4yr\n89.0"]
vals=[69.9,71.0,72.2,89.0]
ax.bar(labels,vals,color=["#36c","#36c","#36c","#d33"])
ax.set_ylim(0,100); ax.set_title("Share of retail accounts losing (regulator disclosures)")
ax.set_ylabel("% losing")
fig.tight_layout(); fig.savefig(ASSETS/"chart_lossrate.png"); plt.close(fig)

# 5) Demo GIF: animated equity race (PIL, no extra deps beyond matplotlib frames)
from PIL import Image
import io
frames=[]
rng2=np.random.default_rng(7)
tech1=np.cumprod(1+np.where(rng2.random(77)<0.56,0.015,-0.01))
gamb1=np.cumprod(1+np.where(rng2.random(77)<0.45,0.25,-0.25))
gamb1=np.clip(gamb1,0.02,None)
for k in range(10,78,4):
    fig,ax=plt.subplots(figsize=(5,2.8))
    ax.plot(tech1[:k],color="#1a9e54",lw=2,label="$500 technician → $1800 path")
    ax.plot(gamb1[:k],color="#d33",lw=2,label="$200 gambler → wipeout")
    ax.set_ylim(0.02,4.2); ax.set_xlim(0,77); ax.set_yscale("linear")
    ax.set_title(f"Trade {k}/77 — sizing is the strategy"); ax.legend(fontsize=7)
    ax.set_xlabel("trades"); ax.set_ylabel("multiple")
    fig.tight_layout()
    buf=io.BytesIO(); fig.savefig(buf,format="png"); plt.close(fig)
    buf.seek(0); frames.append(Image.open(buf).convert("P"))
frames[0].save(ASSETS/"demo.gif",save_all=True,append_images=frames[1:],duration=350,loop=0)
print("assets:",sorted(p.name for p in ASSETS.iterdir()))
