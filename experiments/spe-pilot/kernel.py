"""K — the minimal deterministic kernel.

This is the component the whole SPE argument reduces trust to, so it must
stay small, deterministic, and LLM-free:

  * it binds every verdict to the content hash of the exact code checked
    (no TOCTOU: the proof is about these bytes, not a filename),
  * it runs the frozen tests in a subprocess with a timeout and judges by
    exit code only,
  * it appends every verdict to a witness log, so that "the checker ran"
    is itself checkable later.

Nothing in here consults a model. Model output can create obligations;
only this kernel can discharge them.
"""

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

WITNESS_LOG = Path(__file__).parent / "results" / "witness.jsonl"
TIMEOUT_S = 5


def sha256(text):
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def check(task, code, meta=None):
    """Run the frozen tests of `task` against `code`. Returns a verdict dict.

    The verdict binds task hash + code hash; the raw stderr tail is included
    so callers (the SPE arm) can feed the failure back to the generator.
    """
    program = code + "\n\n" + "\n".join(task["tests"]) + "\nprint('K_PASS')\n"
    task_hash = sha256(task["sig"] + task["doc"] + "\n".join(task["tests"]))
    code_hash = sha256(code)
    started = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-c", program],
            capture_output=True, text=True, timeout=TIMEOUT_S,
        )
        passed = proc.returncode == 0 and "K_PASS" in proc.stdout
        error = "" if passed else (proc.stderr.strip()[-500:] or
                                   f"exit={proc.returncode}")
    except subprocess.TimeoutExpired:
        passed, error = False, f"timeout after {TIMEOUT_S}s"
    verdict = {
        "ts": time.time(),
        "task": task["id"],
        "task_hash": task_hash,
        "code_hash": code_hash,
        "passed": passed,
        "error": error,
        "elapsed_s": round(time.time() - started, 3),
        **(meta or {}),
    }
    WITNESS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(WITNESS_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(verdict, ensure_ascii=False) + "\n")
    return verdict
