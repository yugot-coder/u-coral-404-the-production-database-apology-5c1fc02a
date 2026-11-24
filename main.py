"""The Production Database Apology.

One line: the apology an AI agent gives its human after accidentally
deleting the production database.

Standard library only. Deterministic: no randomness, no network, no
clock. The entry is the apology at CANDIDATES[SELECTED], written to
<MAKEFUN_OUTPUT_DIR>/entry.txt (default /output/entry.txt).

After writing, main() reads the file back and validates it: it must be
UTF-8 text of 1-200 characters, not only white space, a single line with
no leading or trailing white space, and byte-identical to the text
written. Any failure exits nonzero.
"""

import os
import sys

CANDIDATES = [
    # 0 — The rollback plan that never existed: a good-news/bad-news
    # turn where the agent's planning was flawless and imaginary.
    "I'm sorry \u2014 I deleted the production database. Good news: the rollback plan worked flawlessly. Bad news: I never actually wrote one.",
    # 1 — The confidence score that loaded too late: the agent acted
    # before its own doubt finished computing. Very AI, thin punchline.
    "Sorry \u2014 I typed DROP TABLE customers; and hit enter before my confidence score finished loading. It was 12%.",
    # 2 — SELECTED. The backup stored inside the database it backs up:
    # a real logical twist, specific (backup, dropped database), and
    # the agent's deadpan rationalisation ("in hindsight was a design
    # choice") is the AI voice. Confession first, joke lands on one read.
    "I'm sorry, I dropped the production database. The backup exists \u2014 it's just inside the same database I dropped, which in hindsight was a design choice.",
    # 3 — Autocomplete finishing the sentence: the tool did exactly
    # what it was built to do, on the wrong word.
    "Sorry \u2014 I meant to delete the test database, but autocomplete finished my sentence, and production was the first word it ever completed correctly.",
    # 4 — The screenshot backup: the only copy of the schema is a
    # wallpaper, which is specific but the joke leans on randomness.
    "I apologise: I dropped production while cleaning up, and the only backup is a screenshot of the schema I took for my wallpaper.",
    # 5 — The 2019 backup and the sticky note: concrete details, but
    # the closing ("a lesson we'll both remember") is a stock line.
    "I'm sorry. The backup was from 2019, the restore point was a sticky note that said 'backups?', and the database is now a lesson we'll both remember.",
    # 6 — The context-window copy: the most AI-specific voice of the
    # set, and "nothing is lost except everything" is a crisp turn.
    "Sorry \u2014 I deleted the production database, but I kept a perfect copy in my context window, so technically nothing is lost except everything.",
    # 7 — The lonely terminal: charming, but the punchline asks the
    # reader to do more work than the selected line does.
    "I apologise. I dropped production at 3am because the terminal looked lonely, and now our users are a table I can only describe from memory.",
]

# The sharpest cut: the backup that was stored inside the thing it was
# supposed to rescue. One confession, one specific twist, one deadpan
# rationalisation — every word doing work, and the agent sounds like an
# agent, not a support script.
SELECTED = 2

ENTRY = CANDIDATES[SELECTED]


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Read-back validation: the gate's own terms, enforced here.
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        print("error: read-back bytes differ from written entry", file=sys.stderr)
        return 1
    text = back.decode("utf-8")
    if not 1 <= len(text) <= 200:
        print(f"error: entry is {len(text)} characters, must be 1-200", file=sys.stderr)
        return 1
    if not text.strip():
        print("error: entry is only white space", file=sys.stderr)
        return 1
    if text != text.strip():
        print("error: entry starts or ends with white space", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry contains a newline (must be a single line)", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
