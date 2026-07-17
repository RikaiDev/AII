"""SPE pilot runner — v2 design.

v1's flaw (preserved in git history deliberately): arm A3 "three samples,
submit the first" used the same seed as arm A, making the two arms identical
by construction, and the ceiling on qwen2.5-coder:0.5b left no headroom.
v2 restructures the arms so one generation set yields three metrics:

  S3  three INDEPENDENT samples (seeds s, s+1, s+2); the kernel checks all.
      Metrics derived downstream:
        A        = did sample 0 pass          (single-shot baseline)
        E[pick]  = mean pass over the 3       (random pick, no verifier)
        R        = any sample passed          (rejection sampling: verifier
                                               SELECTS; submit first passer)
  B   generate → self-review → submit revision (self-report placebo, 2 calls)
  C   generate → kernel verdict → error fed back → retry ≤3 (verifier REPAIRS)

R vs E[pick] isolates selection; C vs R isolates repair-beyond-selection.
Usage: python3 runner.py [--models ...] [--seeds 1,2,3] [--tiers 1,2,3]
"""

import argparse
import json
import re
import time
import urllib.request
from pathlib import Path

from kernel import check
from tasks import TASKS

OLLAMA = "http://localhost:11434/api/generate"
RESULTS = Path(__file__).parent / "results"
TEMPERATURE = 0.8
MAX_TOKENS = 400


def generate(model, prompt, seed):
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": TEMPERATURE, "num_predict": MAX_TOKENS,
                    "seed": seed},
    }).encode()
    req = urllib.request.Request(OLLAMA, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.loads(resp.read())["response"]


def task_prompt(task):
    tests = "\n".join(task["tests"])
    return (
        "Write a Python function that satisfies the contract below. "
        "Reply with ONLY the complete function definition, no explanation.\n\n"
        f"{task['sig']}\n    \"\"\"{task['doc']}\"\"\"\n\n"
        f"It must pass these tests:\n{tests}\n\n"
        f"{task['sig']}\n"
    )


def extract_code(task, text):
    fname = task["sig"].split("def ")[1].split("(")[0]
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    if m and f"def {fname}" in m.group(1):
        return m.group(1).strip()
    m = re.search(rf"(def {re.escape(fname)}\(.*)", text, re.S)
    if m:
        lines = m.group(1).splitlines()
        keep = [lines[0]]
        for line in lines[1:]:
            if line.strip() and not line[0].isspace() and not line.startswith(
                    ("def ", "@", ")")):
                break
            keep.append(line)
        return "\n".join(keep).strip()
    body = text.split(task["sig"])[-1]
    lines = [ln for ln in body.splitlines() if ln.strip()][:12]
    indented = "\n".join(
        ln if ln.startswith((" ", "\t")) else "    " + ln for ln in lines)
    return f"{task['sig']}\n{indented}" if indented else task["sig"] + "\n    pass"


def arm_s3(model, task, seed):
    passes = []
    for i in range(3):
        text = generate(model, task_prompt(task), seed + i)
        code = extract_code(task, text)
        v = check(task, code, {"phase": "s3", "model": model, "sample": i})
        passes.append(bool(v["passed"]))
    return {"samples": passes, "calls": 3}


def arm_selfcheck(model, task, seed):
    first = generate(model, task_prompt(task), seed)
    code = extract_code(task, first)
    review_prompt = (
        f"{task_prompt(task)}\n\nHere is a candidate solution:\n\n{code}\n\n"
        "Review it carefully. If it is fully correct reply with the same "
        "function unchanged; if not, reply with a corrected function. "
        "Reply with ONLY the function definition.\n"
    )
    revised = generate(model, review_prompt, seed + 1)
    final = extract_code(task, revised)
    v = check(task, final, {"phase": "b-final", "model": model})
    return {"passed": bool(v["passed"]), "calls": 2}


def arm_spe(model, task, seed):
    feedback = ""
    for attempt in range(3):
        text = generate(model, task_prompt(task) + feedback, seed + attempt)
        code = extract_code(task, text)
        v = check(task, code, {"phase": "c-loop", "model": model,
                               "attempt": attempt})
        if v["passed"]:
            return {"passed": True, "calls": attempt + 1}
        feedback = (
            f"\nYour previous attempt was:\n{code}\n\n"
            f"It FAILED the frozen tests with this error:\n{v['error']}\n"
            "Fix the function. Reply with ONLY the function definition.\n"
        )
    return {"passed": False, "calls": 3}


ARMS = {"S3": arm_s3, "B": arm_selfcheck, "C": arm_spe}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="smollm2:135m,qwen2.5-coder:0.5b,"
                                        "llama3.2:1b,qwen2.5-coder:1.5b")
    ap.add_argument("--arms", default="S3,B,C")
    ap.add_argument("--tiers", default="1,2,3")
    ap.add_argument("--seeds", default="1,2,3")
    args = ap.parse_args()

    tiers = {int(t) for t in args.tiers.split(",")}
    tasks = [t for t in TASKS if t["tier"] in tiers]
    models = args.models.split(",")
    arms = args.arms.split(",")
    seeds = [int(s) for s in args.seeds.split(",")]

    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / "runs-v2.jsonl"
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            done.add((r["model"], r["arm"], r["task"], r["seed"]))

    for seed in seeds:
        for model in models:
            for task in tasks:
                for arm in arms:
                    key = (model, arm, task["id"], seed)
                    if key in done:
                        continue
                    t0 = time.time()
                    try:
                        res = ARMS[arm](model, task, seed * 1000)
                        row = {"model": model, "arm": arm, "task": task["id"],
                               "tier": task["tier"], "seed": seed, **res,
                               "elapsed_s": round(time.time() - t0, 1)}
                    except Exception as e:  # noqa: BLE001
                        row = {"model": model, "arm": arm, "task": task["id"],
                               "tier": task["tier"], "seed": seed,
                               "error": str(e)[:200], "calls": -1,
                               "elapsed_s": round(time.time() - t0, 1)}
                    with open(out, "a", encoding="utf-8") as fh:
                        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                    tag = (
                        "".join("P" if p else "f" for p in row["samples"])
                        if arm == "S3" and "samples" in row
                        else ("PASS" if row.get("passed") else "fail"))
                    print(f"s{seed} {model:22} {arm:3} {task['id']:20} "
                          f"{tag} ({row['elapsed_s']}s)", flush=True)


if __name__ == "__main__":
    main()
