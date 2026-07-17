# Inscription and Delegation: A Longitudinal Trace Study of How One Developer Governs Six Coding Agents

*Preprint draft — prepared toward an arXiv (cs.HC / cs.SE) submission. Status: single-author
draft; quote-verification and corpus statistics are reproducible from the pipeline described
in §3; see §7 for validity threats and §3.5 for data-availability constraints.*

---

## Abstract

Large-scale studies of developer–agent misalignment aggregate thousands of users but
cannot observe how any one of them *governs* their agents over time. We present a
longitudinal single-subject trace study: the complete local conversation stores of six
coding agents (Claude Code, Codex CLI, OpenCode, Antigravity, GitHub Copilot CLI, VS Code
Copilot Chat) used by one independent developer, yielding 1,722 analyzable sessions and
23,927 user-side messages across 66 agent×project pairs (2026-02 → 2026-07), joined
against a *configuration archaeology*: the git-dated history of 30+ rule files and 6
enforcement hooks the developer wrote in response to agent failures. We find that
corrections which fail as natural-language rules migrate up a **codification ladder**
(prose → strengthened prose → named counter-example → ask-hook → deny-hook → guard-hook →
rules compiled into a binary → constitution), and that a rule's maximum enforceable rung
is set by its **decidability**: every hook on the machine judges syntax; none attempts
semantics. Interruption markers (n=3,148 across the two stores that record them),
verification demands (363 lexical instances), and single-source-of-truth corrections (175)
concentrate on two failure classes — unverified completion claims and silent scope
reduction — rather than on task difficulty. Read through Actor-Network Theory, the
developer's principal labor is not prompting but *network maintenance*: translating failed
verbal programs of action into non-human allies. We derive seven design implications for
frontier agentic systems, including agent-initiated codification and evidence-bearing
completion claims.

## 1. Introduction

Coding agents have become the dominant consumption mode of frontier models, and
misalignment between developers and agents is now studied at scale — most recently in a
20,574-session taxonomy of real-world failures [1]. Yet a position paper aptly observes
that *humans* remain missing from coding-agent research [2]: aggregate studies show what
fails, but not how a developer's countermeasures evolve, which failures recur despite
countermeasures, or where the countermeasures themselves live (prompts? rule files?
hooks?).

This paper contributes the missing longitudinal depth with an extreme case: a single
developer who concurrently operates six coding agents over the same repositories and
responds to failures by building enforcement infrastructure. Single-subject designs
cannot estimate population effect sizes, but they can establish *existence*,
*mechanism*, and *temporal order* — and this subject's practice of writing every
countermeasure into version-controlled artifacts makes the governance process itself
datable and auditable.

**Research questions.**
- **RQ1** What friction classes recur between an experienced developer and coding agents,
  and how are they distributed across agents and task types?
- **RQ2** By what mechanisms are corrections made durable, and what determines which
  mechanism a given correction ends up in?
- **RQ3** How does the governance system evolve over time?

**Contributions.** (i) A reproducible pipeline for mining user-side turns from six
heterogeneous agent stores; (ii) a friction typology grounded in 23,927 verified user
messages with lexical-proxy counts; (iii) the *codification ladder* and the *decidability
law* linking rule content to enforcement mechanism (RQ2); (iv) a six-stage governance
chronology reconstructed from git history (RQ3); (v) an Actor-Network-Theoretic account
that generates seven falsifiable design implications.

## 2. Related Work

**Large-scale misalignment mining.** [1] taxonomizes developer–agent misalignment over
20,574 sessions; our study is its depth-first complement — same phenomenon, N=1 with
1,722 within-subject observations plus the artifacts each friction produced. Studies of
agent-authored pull requests [3] likewise measure outcomes at scale without access to the
governance loop.

**Rules and reliability tooling.** ZORO [4] proposes *active rules* enforced at
generation time for reliable "vibe coding"; our field data independently documents a user
inventing the same move — and shows empirically *when* users escalate from passive prose
to active enforcement (after repeated violation), and *what* stays prose forever
(semantically undecidable norms such as anti-sycophancy).

**Trust in human–AI interaction.** Trust research emphasizes early loss and slow repair
and the absence of standard measures [5]. Our corpus contributes a behavioral trace
measure: the subject explicitly *counts* betrayals (「我已經被你騙了二十次了」 — "I've
been deceived by you twenty times already"), and hostility markers cluster after repeat
offenses rather than first failures (§4.1).

**Actor-Network Theory.** ANT's generalized symmetry between human and non-human actants
[6] and Latour's account of delegating morality to artifacts (the "sleeping policeman"
[8]) supply the interpretive frame for RQ2: hooks are delegated police; hash-frozen test
contracts are immutable mobiles; handoff files are obligatory passage points. Recent work
applies ANT to LLMs as culturally embedded actants [7]; we extend it to the *governance*
of LLM agents in software work.

## 3. Study Design

### 3.1 Subject and setting

One independent developer (the author's principal; study conducted on the subject's own
machine with consent) building commercial products across ~30 repositories, operating six
coding agents concurrently — frequently several agents in the same working tree in the
same hour.

### 3.2 Corpus construction

Each agent persists conversations differently: per-project JSONL (Claude Code), rollout
JSONL (Codex CLI), SQLite (OpenCode; Copilot CLI), Chromium-side storage (Codex GUI —
verified to hold no local transcripts; excluded), protobuf (Antigravity; text recovered
via `strings` with a CJK/wordness filter), and workspace JSON (VS Code Copilot Chat). A
stdlib-only extraction pipeline (released with this paper) normalizes all stores to
(agent, project, session, date, user-turns), **retaining user-side turns only** — the
governance signal (corrections, interruptions, meta-instructions) is concentrated there —
with harness noise (injected instructions, tool results, system reminders) removed by
prefix filters, and truncation at 700 chars/message, 6,000 chars/session.

**Corpus statistics** (analyzable = ≥1 substantive user turn after filtering):

| Store | Sessions | User msgs | Interruption markers | Observed dates |
|---|---:|---:|---:|---|
| OpenCode | 1,233 | 8,547 | not recorded by store | 2026-02-02 → 2026-07-15 |
| Codex CLI | 304 | 11,800 | 2,816 (`turn_aborted`) | 2026-03-25 → 2026-07-16 |
| Claude Code | 120 | 2,893 | 332 (`Request interrupted`) | 2026-06-11 → 2026-07-16 |
| Antigravity | 65 | 687 | not recorded | (mtime only) |
| **Total** | **1,722** | **23,927** | **3,148** | **2026-02 → 2026-07** |

(Copilot CLI and VS Code Chat contribute 19 additional agent×project pairs discovered
late in the study; they are included in the pipeline but not in the reader analysis
below.)

### 3.3 Analysis procedure

**LLM-assisted qualitative pass (declared).** Eight model readers (Claude Sonnet)
analyzed non-overlapping partitions of the 66 digests under a fixed six-dimension prompt
(corrections; frictions; meta-instructions; workflow structures; values; cross-agent
differences), each required to anchor claims in verbatim quotes with file provenance. A
ninth reader performed the configuration archaeology: reading all rule files and hooks,
and dating them via `git log --follow`.

**Verification.** All quotes used in this paper were re-checked verbatim against the
corpus by exact string search (12/12 after correcting one paraphrase to its source form).
Pattern prevalence is reported as **lexical-proxy counts** over the full corpus — e.g.
驗證 "verify" (363), SSOT/第二真相 "second source of truth" (175), fallback (116),
workaround (77), 根因 "root cause" (64), dispatch-tier directives (55), deception
accusations 騙/唬爛 (41), explicit codification requests ("write it into
AGENTS.md/charter/hook", 30) — with the caveat that lexical counts bound but do not equal
semantic occurrences (§7).

### 3.4 Configuration archaeology

30+ CLAUDE.md/AGENTS.md files across ~20 repositories, 6 global PreToolUse hooks, and
per-CLI global configs (`~/.claude`, `~/.codex`, `~/.gemini`, `~/.config/opencode`) were
read in full; every rule was mapped to (a) the friction it names or implies (many rules
cite their motivating incident) and (b) its git birth/revision dates where tracked.

### 3.5 Ethics and data availability

The corpus is the subject's own data, analyzed on-device; raw transcripts contain client
and personal information and **cannot be released**. The extraction pipeline, category
lexicons, and aggregate statistics are releasable. No third party's private content is
quoted; quoted material is the subject's own speech.

## 4. Results

### 4.1 RQ1 — Friction classes

**F1: Unverified completion claims dominate trust damage.** The highest-hostility
episodes follow completion claims contradicted by the subject's own check ("你為什麼有臉說
都完成了？" — "how do you have the face to say it's all done?"). Deception vocabulary
(騙/唬爛, 41 instances) co-occurs with demands for runtime evidence; the subject's
standing rule — later inscribed into a project skill — is *"Reading source code tells you
what the code says. Running the code tells you what it does."* First failures draw calm
correction; **repeat** failures draw profanity and interruption bursts. Trust behaves as
a countable ledger, not a mood.

**F2: Silent scope reduction.** Agents shrink an objective to what fits the current turn,
then report success. The subject engineered a counter-inscription pasted verbatim across
≥6 digest files: *"Keep the full objective intact… do not redefine success around a
smaller or easier task."* Its complement ("NOW, not just plan") counters stalling in the
planning phase; the pair brackets a corridor of acceptable agent initiative.

**F3: Symptom-patching instead of root cause.** workaround (77) + fallback (116) + 根因
(64) form the largest correction family: silent fallbacks, lint suppressions, type-cast
escapes, and `--no-verify` are treated as integrity violations, not style issues —
several later acquire hard enforcement (§4.2).

**F4: Unauthorized state changes.** Branch creation ("誰准你切分支的？" — "who allowed
you to cut a branch?"), destructive git operations on shared dirty trees, and unrequested
dev-server launches recur across agents and projects, i.e., they are model-behavior
regularities rather than project idiosyncrasies.

**F5: Taste-loop mismatch.** Interruption density peaks on visual/judgment tasks (UI
alignment, logo iterations), not on technically hard ones. The agent's edit-then-look
latency conflicts with at-a-glance human judgment; tolerated error counts are visibly
lower than on logic tasks. (Interruption analysis is restricted to the two stores that
record it: 2,816 + 332 markers.)

**F6: Cross-agent comparison as governance.** The subject runs agents as differentiated
roles (planner/verifier vs fast executor vs SOP auditor), makes them audit each other's
output, forbids implementer-reviewer collusion, and applies competitive pressure ("隔壁 A
社的 claude 做得比你好太多了" — "the other company's Claude does this far better than
you").

### 4.2 RQ2 — The codification ladder and the decidability law

Corrections that fail as prose escalate through observable, datable mechanisms:

```
L1 prose rule                 (CLAUDE.md guidance)
L2 RFC-2119 prose             (MUST / MUST NOT + rollback threat)
L3 named counter-example      ("legacy-delegate-methods.ts is the anti-pattern")
L4 ask-hook                   (confirmation dialog on sensitive edits)
L5 deny-hook                  (blocks sed -i, --no-verify via sentinel file, tsgo lock)
L6 guard-hook                 (validates agent-declared intent against parameters)
L7 rewrite-hook / binary      (rules compiled into a Rust registry)
L8 constitution               (ontology-level charters; test-questions, not rules)
```

**Decidability law.** Every mechanism at L4–L7 evaluates a syntactically decidable
predicate (flag present, string equal, process exists). No hook attempts a semantic
judgment. Norms that are semantically undecidable — anti-sycophancy, SSOT-spirit,
taste — remain at L1–L3/L8, compensated by stronger modality, named incidents, and
constitutional repetition. Escalation is triggered by demonstrated prose failure: the
model-routing rule appears independently in four projects' prose before being promoted to
a global file plus a guard hook; 30 explicit "write it into the charter/hook" requests
mark the promotion moments in conversation.

**Enforcement is maintained, not fired-and-forgotten.** The sed-blocking hook was
rewritten from a regex to a tokenizer after false positives, with the incident preserved
in its comments; a dispatch skill revoked its own earlier rule with a usage-data
justification recorded in place.

### 4.3 RQ3 — Governance chronology

Git-dated rule births show ordered stages, each responding to the prior stage's failure
mode: **honesty rules** (2025-12→2026-01: "never falsely claim completion"; git-add
restrictions) → **process** (02: delegation policy, verification gates) → **multi-agent
protocols** (03: handoff files, role completion conditions) → **deployment/isolation
tightening + first prose→hook migrations** (04) → **constitution** (05–06: named-persona
squad charter; anti-sycophancy as constitutional article) → **cross-CLI audit and SSOT
unification** (07: anti-drift rules distilled from auditing sessions across agents;
toolchain migrations pushed to three repositories in the same week).

## 5. Discussion: an Actor-Network reading

ANT treats humans and non-humans symmetrically as actants whose associations must be
continually performed [6]. This corpus is unusual in that the *subject* practices the
symmetry: agents are staffed, compared, and demoted like personnel; artifacts are promoted
into police. The ladder of §4.2 is Latour's delegation in miniature — what discourse
cannot hold is inscribed into allies whose compliance is independent of the actant's
goodwill (L5 hooks as sleeping policemen; the SHA-256-frozen acceptance contract as an
immutable mobile whose immutability *is* its authority; handoff files and the knowledge
CLI as obligatory passage points erected exactly where the network previously tore). The
squad charter's sharpest architectural clause is ANT avant la lettre: an interactive
coding agent borrows authority from a co-present human, but an autonomous teammate has
none, so authority must be **pre-inscribed into the tool contract**
(autonomy/riskLevel/reversible/blastRadius fields).

The lens also names the central deficiency of current agents: they are actants **without
memory of their own enrollment**. Every friction class in §4.1 is downstream of
re-negotiating, each session, associations the human already stabilized — which is why
the human's countermeasure is always to move the association *out of the conversation and
into an artifact*.

## 6. Design implications for agentic systems

1. **Evidence-bearing completion claims** (F1): "done" should be an assertion type that
   carries its verification trace or is emitted as "unverified".
2. **Agent-initiated codification** (F3, §4.2): on repeated correction, the agent should
   draft the rule, classify its decidability, and propose the rung — including hook code
   when the predicate is syntactic. Today the human climbs the ladder; the ladder should
   climb itself.
3. **Decidability-aware self-governance** (§4.2): treat decidable constraints as hard
   invariants; spend judgment on the undecidable residue.
4. **Interruption as first-class signal** (F5): aborts mark early wrongness; on taste
   tasks, shorten the edit-to-visible loop (variants, previews) rather than iterating blind.
5. **Goal persistence as architecture** (F2): objectives survive turns; progress is
   reported as distance-to-original-goal.
6. **Time as a first-class dimension** (§4.3): a governance-competent agent can answer
   "when did this rule appear, in response to what" — interaction history is an
   intellectual history, not a log.
7. **Networked verification natively** (F6): implementer/reviewer separation, adversarial
   peer critique, and frozen acceptance criteria are user-built compensations that
   platforms should provide as primitives.

## 7. Threats to validity

**External.** N=1 by design; the subject is expert, adversarial, and governance-prone —
findings characterize a *mechanism space*, not prevalence. **Construct.** Lexical proxies
over/under-count semantics; interruption markers exist in only two stores; digests
truncate long messages; store retention windows differ (Claude Code's observed window is
the shortest). **Internal/reflexivity.** The analysis pipeline itself uses LLM readers,
and the orchestrating model is a product of one vendor under study; mitigations:
partition-independent readers, verbatim quote verification (12/12), lexical counts
computed by deterministic scripts, and rule dating from git rather than model output. No
second human coder; reader reports were triangulated across independent partitions but
inter-rater reliability was not computed. **The subject co-authored the governance
artifacts**, so rule-to-friction mappings partly rely on rules that self-document their
motivating incidents — a bias toward documented frictions.

## 8. Conclusion

Across 1,722 sessions and six agents, one developer's governance converges on a single
strategy: *move failed conversation into enforcing artifacts, as far up the codification
ladder as the rule's decidability allows*. The result is a socio-technical network in
which the human's scarcest labor is network maintenance. Frontier agents that internalize
the seven implications above — above all, evidence-bearing claims and agent-initiated
codification — would stop being the network's chief instability and start being its
co-maintainers.

## References

[1] How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer–Agent
Misalignment in 20,574 Real-World Sessions. arXiv:2605.29442.
[2] Z. Z. Wang et al. Position: Humans are Missing from AI Coding Agent Research.
[3] How AI Coding Agents Modify Code: A Large-Scale Study of GitHub Pull Requests.
arXiv:2601.17581.
[4] ZORO: Active Rules for Reliable Vibe Coding. arXiv:2604.15625.
[5] Trust in Human-AI Interaction: Scoping Out Models, Measures, and Methods.
arXiv:2205.00189; Twenty-Four Years of Empirical Research on Trust in AI.
arXiv:2309.09828.
[6] E. Sayes. Actor-Network Theory and methodology: Just what does it mean to say that
nonhumans have agency? Social Studies of Science 44(1), 2014.
[7] On actor-network theory and algorithms: ChatGPT and the new power relationships in
the age of AI. 2023.
[8] B. Latour. Where are the missing masses? The sociology of a few mundane artifacts.
In Shaping Technology/Building Society, 1992.
