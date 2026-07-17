# SPE Pilot — does a deterministic verifier lift correctness at every capability level?

Pilot experiment for **Self-Proving Engineering (SPE)**: the claim that
reliability should come from *structure* (frozen contract + minimal
deterministic kernel + bounded feedback) rather than from model capability or
model self-report.

## Vocabulary: agent work as a debt relation

SPE borrows its terms from contract law rather than from testing, because the
failure it addresses is not "the code is wrong" but "the work was declared
finished by the party who owed it".

| Term | Meaning in SPE |
|---|---|
| **Contract** | The acceptance criteria, frozen (content-hashed) *before* work starts |
| **Obligation** | A criterion the agent has taken on and not yet satisfied |
| **Discharge** | Proof that an obligation is met — **only the kernel may certify it** |
| **Default** | Declaring an obligation discharged when it is not (失信) |
| **Trust ledger** | The human's running count of defaults ("I've been deceived twenty times") |

The pun is load-bearing: **`default` is both *breach of obligation* and *the
behaviour you get when nothing is specified*.** An agent asked to certify its
own work defaults in both senses at once.

This reframes the experiment's arms. Arm **B** (self-check) is *letting the
debtor certify their own repayment* — which is why it does not merely fail to
help but actively destroys correct work (−31.4pp on llama3.2:1b). Arm **R** is
certification by a party that cannot lie. **SPE's subject is not testing; it is
who holds discharge authority.**

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

## Results (6 models × 35 tasks × 3 seeds = 102 cells/model/arm)

Run on an RTX 4080 box (models via ollama, CPU/GPU as ollama chooses).
Full table in `results/RESULTS.txt`; raw rows in `results/runs-v2.jsonl`.

| model | A | E[pick] | **R** | **B** | **R−E[pick]** | **B−A** |
|---|---|---|---|---|---|---|
| smollm2:135m | 46.1% | 44.8% | **63.7%** | 46.1% | **+19.0** | 0.0 |
| llama3.2:1b | 76.5% | 75.8% | **87.3%** | 45.1% | +11.4 | **−31.4** |
| qwen2.5-coder:0.5b | 87.3% | 86.6% | **95.1%** | 81.4% | +8.5 | −5.9 |
| qwen2.5-coder:1.5b | 95.1% | 95.8% | **100%** | 92.2% | +4.2 | −2.9 |
| qwen2.5-coder:7b | 100% | 99.3% | **100%** | 96.1% | +0.7 | −3.9 |
| qwen2.5-coder:14b | 98.0% | 97.7% | **100%** | 100% | +2.3 | +2.0 |

### Verdicts against the pre-registered hypotheses

- **H1 (selection gain) — supported.** R > E[pick] at every rung; the gain
  decays monotonically with capability (+19.0pp at 135M → +0.7pp at 7B). The
  deterministic kernel converts occasional competence into reliable delivery,
  and the effect is largest exactly where competence is least reliable.
- **H2 (self-report is not a verifier) — supported, and stronger than stated.**
  Self-check is not merely neutral, it is *harmful*: B−A is negative for five of
  six models (llama3.2:1b −31.4pp overall, −52.4pp on tier 2). Only the 14B
  model avoids damaging its own correct answers (+2.0). Asking a model to
  discharge its own obligation destroys work.
- **H3 (weak-model leverage) — supported.** Relative uplift is largest for the
  weakest model (44.8% → 63.7%, +42% relative); 7B has no headroom left.
- **H4 (repair has a capability floor) — supported.** C−R ≤ 0 for the small
  models (135M: −13.7) and reaches 0 only at 1.5B+. Selection needs no
  capability; repair does. Note C spends fewer calls (mean 1.0–2.1 vs R's
  fixed 3), so C trades accuracy for budget rather than being strictly worse.
- **H5 (reward-hacking asymmetry)** — design claim, not measured here.

An incidental observation worth the paper: **14B's single-shot A (98.0%) is
below 7B's (100%), yet both reach 100% under R** — the kernel compensates for
capability's randomness, which is precisely the SPE thesis.
