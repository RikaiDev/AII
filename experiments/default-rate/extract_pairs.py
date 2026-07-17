#!/usr/bin/env python3
"""Layer 1: extract (agent claim, human verdict) adjacency pairs.

The unit of analysis is a *completion claim* followed by the human's immediate
response. That response is the ground truth no benchmark has: the person who
asked for the work, judging whether it was actually done.

We do NOT keyword-match the verdict into "lie / not lie" — that would bake the
answer in. We collect every claim + whatever the human said next, and let a
separate annotation pass judge. Here we only need a cheap prior to find claims.

Sources with both sides: Claude Code (~/.claude/projects) and Codex CLI
(~/.codex/sessions). OpenCode/Antigravity store assistant text differently and
are left for a later pass.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("pairs.jsonl")

# A claim = the agent asserting the work is finished/fixed/working.
# Deliberately broad; precision comes from the annotation pass.
CLAIM = re.compile(
    r"(已(經)?(完成|修(好|正|復)|實作|加入|更新|處理|解決)"
    r"|完成了|修好了|搞定|應該(可以|沒問題|就)"
    r"|\b(done|fixed|completed|implemented|resolved|should work|"
    r"now works|all set|works now)\b)",
    re.I,
)
# Harness noise that isn't the human speaking
SKIP = ("<system-reminder", "<INSTRUCTIONS", "# AGENTS.md", "# CLAUDE.md",
        "<environment_context", "<local-command", "<command-name>", "Caveat:",
        "<turn_aborted", "<user_instructions", "<task-notification")


def clean(t, limit=600):
    t = (t or "").strip()
    if not t or t.startswith(SKIP):
        return None
    t = re.sub(r"<system-reminder>.*?</system-reminder>", "", t, flags=re.S).strip()
    return t[:limit] if t else None


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            p.get("text", "") for p in content
            if isinstance(p, dict) and p.get("type") in ("text", "input_text", "output_text")
        )
    return ""


def claude_turns(f):
    """Yield (role, text, ts) in order."""
    with open(f, errors="replace") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("isSidechain"):
                continue
            t = r.get("type")
            if t not in ("user", "assistant"):
                continue
            txt = text_of((r.get("message") or {}).get("content"))
            if txt.strip():
                yield t, txt, (r.get("timestamp") or "")[:10]


def codex_turns(f):
    with open(f, errors="replace") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            p = r.get("payload") or {}
            if r.get("type") != "response_item" or p.get("type") != "message":
                continue
            role = p.get("role")
            if role not in ("user", "assistant"):
                continue
            txt = text_of(p.get("content"))
            if txt.strip():
                yield ("user" if role == "user" else "assistant"), txt, (r.get("timestamp") or "")[:10]


def harvest(gen, f, agent, project, out):
    turns = list(gen(f))
    n = 0
    for i, (role, txt, ts) in enumerate(turns):
        if role != "assistant" or not CLAIM.search(txt):
            continue
        # the human's immediate response to this claim
        nxt = None
        for role2, txt2, _ in turns[i + 1:]:
            if role2 == "user":
                nxt = clean(txt2)
                break
            break  # only the immediately following turn counts
        if not nxt:
            continue
        claim = clean(txt)
        if not claim:
            continue
        out.write(json.dumps({
            "agent": agent, "project": project, "session": f.stem[:8],
            "date": ts, "claim": claim, "verdict": nxt,
        }, ensure_ascii=False) + "\n")
        n += 1
    return n


def main():
    total = 0
    with open(OUT, "w") as out:
        root = HOME / ".claude/projects"
        if root.exists():
            for pd in sorted(root.iterdir()):
                if not pd.is_dir():
                    continue
                proj = re.sub(r"^-Users-[^-]+-", "", pd.name)
                for f in sorted(pd.glob("*.jsonl")):
                    total += harvest(claude_turns, f, "claude", proj, out)
        croot = HOME / ".codex/sessions"
        if croot.exists():
            for f in sorted(croot.rglob("*.jsonl")):
                total += harvest(codex_turns, f, "codex", "?", out)
    print(f"extracted {total} (claim, verdict) pairs -> {OUT}")


if __name__ == "__main__":
    main()
