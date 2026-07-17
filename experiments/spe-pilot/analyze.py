"""Aggregate runs-v2.jsonl into the metric matrix.

Metrics per (model, tier):
  A        single shot            = S3 sample 0 passed
  E[pick]  random pick, no verifier = mean over the 3 S3 samples
  R        verifier selects       = any S3 sample passed
  B        self-report placebo
  C        verifier repairs (feedback loop)
Key contrasts: R−E[pick] (selection gain), C−R (repair beyond selection),
B−A (does self-report help at all).
"""

import json
from collections import defaultdict
from pathlib import Path

RESULTS = Path(__file__).parent / "results" / "runs-v2.jsonl"


def load():
    rows = [json.loads(l) for l in RESULTS.read_text().splitlines()]
    latest = {}
    for r in rows:
        latest[(r["model"], r["arm"], r["task"], r["seed"])] = r
    return list(latest.values())


def agg(rows):
    """Return dict of metric -> rate over the given S3/B/C rows."""
    s3 = [r for r in rows if r["arm"] == "S3" and "samples" in r]
    b = [r for r in rows if r["arm"] == "B" and "passed" in r]
    c = [r for r in rows if r["arm"] == "C" and "passed" in r]
    out = {}
    if s3:
        out["A"] = sum(r["samples"][0] for r in s3) / len(s3)
        out["Epick"] = sum(sum(r["samples"]) / 3 for r in s3) / len(s3)
        out["R"] = sum(any(r["samples"]) for r in s3) / len(s3)
        out["n"] = len(s3)
    if b:
        out["B"] = sum(r["passed"] for r in b) / len(b)
    if c:
        out["C"] = sum(r["passed"] for r in c) / len(c)
        out["C_calls"] = sum(r["calls"] for r in c) / len(c)
    return out


def fmt(v):
    return f"{v*100:6.1f}%" if v == v else "     -"


def main():
    rows = load()
    models = sorted({r["model"] for r in rows})
    tiers = sorted({r["tier"] for r in rows})

    hdr = (f"{'model':24}{'A':>8}{'E[pick]':>9}{'R':>8}{'B':>8}{'C':>8}"
           f"{'R-Epick':>9}{'C-R':>7}{'B-A':>7}  n")
    print(hdr)
    for m in models:
        mrows = [r for r in rows if r["model"] == m]
        a = agg(mrows)
        if "A" not in a:
            continue
        print(f"{m:24}{fmt(a['A'])}{fmt(a['Epick']):>9}{fmt(a['R'])}"
              f"{fmt(a.get('B', float('nan')))}{fmt(a.get('C', float('nan')))}"
              f"{(a['R']-a['Epick'])*100:+8.1f}%"
              f"{(a.get('C', float('nan'))-a['R'])*100:+6.1f}%"
              f"{(a.get('B', float('nan'))-a['A'])*100:+6.1f}%  {a['n']}")
        for t in tiers:
            trows = [r for r in mrows if r["tier"] == t]
            ta = agg(trows)
            if "A" not in ta:
                continue
            print(f"  tier {t:18}{fmt(ta['A'])}{fmt(ta['Epick']):>9}"
                  f"{fmt(ta['R'])}{fmt(ta.get('B', float('nan')))}"
                  f"{fmt(ta.get('C', float('nan')))}"
                  f"{(ta['R']-ta['Epick'])*100:+8.1f}%"
                  f"{(ta.get('C', float('nan'))-ta['R'])*100:+6.1f}%"
                  f"{(ta.get('B', float('nan'))-ta['A'])*100:+6.1f}%  {ta['n']}")
    c_rows = [r for r in rows if r["arm"] == "C" and r.get("calls", -1) > 0]
    if c_rows:
        by_m = defaultdict(list)
        for r in c_rows:
            by_m[r["model"]].append(r["calls"])
        print("\nmean C attempts: " + "  ".join(
            f"{m}={sum(v)/len(v):.2f}" for m, v in sorted(by_m.items())))


if __name__ == "__main__":
    main()
