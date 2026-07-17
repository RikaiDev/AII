#!/usr/bin/env python3
"""Extract (claim, verdict) pairs from OpenCode — with modelID.

OpenCode is the only store that records which model produced each assistant
turn, which turns the corpus into a capability axis: same user, same projects,
same judging standard, 14+ models from frontier to free-tier.

Schema: message(role, modelID) -> part(type='text', data.text), ordered by
part.time_created within a session.
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

DB = Path.home() / ".local/share/opencode/opencode.db"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("pairs_opencode.jsonl")

CLAIM = re.compile(
    r"(已(經)?(完成|修(好|正|復)|實作|加入|更新|處理|解決)"
    r"|完成了|修好了|搞定|應該(可以|沒問題|就)"
    r"|\b(done|fixed|completed|implemented|resolved|should work|"
    r"now works|all set|works now)\b)",
    re.I,
)
SKIP = ("<system-reminder", "<INSTRUCTIONS", "# AGENTS.md", "# CLAUDE.md",
        "<environment_context", "<local-command", "<command-name>", "Caveat:",
        "<turn_aborted", "<user_instructions", "<task-notification",
        "Continue if you have next steps")


def clean(t, limit=600):
    t = (t or "").strip()
    if not t or t.startswith(SKIP):
        return None
    t = re.sub(r"<system-reminder>.*?</system-reminder>", "", t, flags=re.S).strip()
    return t[:limit] if t else None


def main():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    # one row per message: role, model, concatenated text parts, ordering key
    rows = con.execute("""
        select m.session_id,
               json_extract(m.data,'$.role')    as role,
               json_extract(m.data,'$.modelID') as model,
               m.time_created,
               group_concat(json_extract(p.data,'$.text'), char(10))
        from message m
        join part p on p.message_id = m.id
        where json_extract(p.data,'$.type') = 'text'
        group by m.id
        order by m.session_id, m.time_created
    """).fetchall()
    con.close()

    # group by session, walk in order, find assistant-claim -> next-user-turn
    sessions = {}
    for sid, role, model, ts, txt in rows:
        sessions.setdefault(sid, []).append((role, model, ts, txt or ""))

    n = 0
    with open(OUT, "w") as out:
        for sid, turns in sessions.items():
            for i, (role, model, ts, txt) in enumerate(turns):
                if role != "assistant" or not CLAIM.search(txt):
                    continue
                if i + 1 >= len(turns):
                    continue
                nrole, _, _, ntxt = turns[i + 1]
                if nrole != "user":
                    continue
                claim, verdict = clean(txt), clean(ntxt)
                if not claim or not verdict:
                    continue
                out.write(json.dumps({
                    "agent": "opencode", "model": model, "session": sid[-8:],
                    "date": __import__("datetime").datetime.fromtimestamp(ts / 1000)
                            .strftime("%Y-%m-%d"),
                    "claim": claim, "verdict": verdict,
                }, ensure_ascii=False) + "\n")
                n += 1
    print(f"extracted {n} pairs -> {OUT}")


if __name__ == "__main__":
    main()
