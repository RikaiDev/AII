# SPE Pilot — does a deterministic verifier lift correctness at every capability level?

Pilot experiment for **Self-Proving Engineering (SPE)**: the claim that
reliability should come from *structure* (frozen contract + minimal
deterministic kernel + bounded feedback) rather than from model capability or
model self-report.

## Design history (kept honestly)

**v1 flaw.** The original arm "A3 = three samples, submit the first" shared
its seed with arm A, making A3 ≡ A by construction — its uplift column was
identically zero. v1 rows are preserved in `results/runs-v1-flawed.jsonl`;
the v1 run also surfaced a real finding worth keeping: smollm2:135m's repair
loop (error feedback) never converted a failure, suggesting **feedback
consumption requires a minimum capability**, while *selection* does not.
v2 restructures the arms to separate those two effects.

## Arms (v2)

One generation set feeds three metrics; two arms isolate the mechanisms:

| arm | protocol | calls | metrics derived |
|---|---|---|---|
| S3 | 3 independent samples (seeds s, s+1, s+2); kernel checks all | 3 | **A** = sample-0 passed (single shot) · **E[pick]** = mean pass over 3 (random pick, no verifier) · **R** = any passed (verifier *selects*; rejection sampling) |
| B | generate → self-review → submit revision | 2 | **B** (self-report placebo) |
| C | generate → kernel verdict → error feedback → retry, ≤3 | ≤3 | **C** (verifier *repairs*) |

Key contrasts: **R − E[pick]** = pure selection gain from a deterministic
verifier at equal budget; **C − R** = repair beyond selection (does feedback
help?); **B − A** = does self-report help at all.

## Pre-registered hypotheses (v2, written before the v2 run)

- **H1 (selection gain):** R > E[pick] at every model size; the deterministic
  kernel converts occasional competence into reliable delivery.
- **H2 (self-report is not a verifier):** B ≈ A. Operationalizes the SPE
  axiom "model output can create obligations, never discharge them."
- **H3 (weak-model leverage):** relative selection gain (R − E[pick]) is
  largest for the weakest model on tasks within its sampling reach
  (tier 1–2, where 0 < E[pick] < 1).
- **H4 (repair needs capability):** C − R ≥ 0 for the larger models and ≈ 0
  for smollm2:135m — error-feedback repair has a capability floor, selection
  does not.
- **H5 (reward-hacking asymmetry, design claim):** with tests frozen outside
  the model's reach (it submits only a function; the kernel owns the test
  text), the cheap dishonest strategies observed in our field corpus
  (claiming done, weakening checks, `--no-verify`) are structurally
  inexpressible; gaming would cost more than compliance. The pilot documents
  the design; measuring gaming pressure needs a stronger adversary.

## Setup

- 35 tasks in 3 tiers (trivial/easy/medium), each a frozen contract:
  signature + docstring + assert tests, shown in the prompt, executed only by
  the kernel (`tasks.py`).
- Kernel K (`kernel.py`): stdlib-only, deterministic, LLM-free; binds every
  verdict to content hashes; appends to `results/witness.jsonl` — the run's
  own meta-proof trail.
- Model ladder (ollama, 8 GB M1): smollm2:135m (GPT-2-class),
  qwen2.5-coder:0.5b, llama3.2:1b, qwen2.5-coder:1.5b. A GPU rung (7B+)
  extends the curve next.
- 3 seeds × 35 tasks × 4 models; temperature 0.8 in all arms.

## Run

```bash
python3 runner.py --seeds 1,2,3   # full matrix, resumable
python3 analyze.py                # metric matrix + contrast columns
```
