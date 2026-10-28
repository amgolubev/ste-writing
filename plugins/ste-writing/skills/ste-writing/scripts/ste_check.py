#!/usr/bin/env python3
"""Report STE-style observations for Markdown or plain-text files.

The script emits observations, never verdicts: it cannot see meaning, so a
person decides each fix. The exit code is 0 unless a path cannot be read.

Usage:
    ste_check.py [--rule-limit N] [--desc-limit N] [--para-limit N]
                 [--json] [--summary] PATH [PATH ...]

A PATH can be a directory; the script then reads its *.md and *.txt files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

WORD_LIST = Path(__file__).resolve().parent.parent / "references" / "word-list.md"

ABBREVIATIONS = ("e.g.", "i.e.", "etc.", "vs.", "cf.", "approx.", "no.", "fig.", "mr.", "ms.", "dr.")
RULE_WORDS = re.compile(r"\b(must|must not|cannot|can't|shall)\b", re.I)
MODALS = re.compile(r"\b(should|shouldn't|may|might|could|would)\b", re.I)
FUTURE = re.compile(r"\b(will|won't)\b", re.I)
SEMICOLON = re.compile(r";")
LATE_CONDITION = re.compile(r"\b(if|unless)\b", re.I)
BE = r"(?:is|are|was|were|be|been|being|gets|get|got)"
IRREGULAR = (
    "built bought caught chosen done drawn driven eaten fallen felt found forgotten "
    "given gone held hidden hit kept known laid led left lost made meant met paid put "
    "read run said seen sent set shown shut sold spent split spoken taken taught thrown "
    "told understood won worn written"
)
PASSIVE = re.compile(
    rf"\b{BE}\s+(?:\w+ly\s+)?(\w+ed|{'|'.join(IRREGULAR.split())})\b(?!\s+(?:to|that)\b)", re.I
)
NOMINAL = re.compile(
    r"\b(?:(?:perform|performs|performed|conduct|conducts|carry out|carries out|make|makes|"
    r"do|does|give|gives|take|takes)\s+(?:a|an|the)\s+\w+(?:tion|sion|ment|ance|al))\b"
    r"|\b\w+(?:tion|sion|ment|ance|ence)\s+(?:occurs|occur|takes place|take place|is performed|happens)\b"
    r"|\b(?:a|an|the)\s+\w+\s+of\s+(?:a|an|the)\s+\w+\s+(?:occurs|takes place|happens)\b",
    re.I,
)
# Words that end in -ed but are rarely participles in a passive.
NOT_PARTICIPLES = {"need", "based", "red", "bed", "speed", "seed", "feed", "shed", "embed", "proceed", "exceed"}


@dataclass
class Observation:
    file: str
    line: int
    code: str
    message: str
    excerpt: str


def load_word_list(path: Path) -> list[tuple[re.Pattern[str], str, str]]:
    pairs: list[tuple[re.Pattern[str], str, str]] = []
    if not path.exists():
        return pairs
    for raw in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if len(cells) != 2 or not raw.lstrip().startswith("|"):
            continue
        complex_word, simple = cells
        if complex_word.lower() in ("complex", "") or set(complex_word) <= {"-", " "}:
            continue
        escaped = re.escape(complex_word).replace(r"\ ", r"\s+")
        tail = r"(?!\w)" if complex_word.endswith(".") else r"\b"
        pattern = re.compile(rf"\b{escaped}{tail}", re.I)
        pairs.append((pattern, complex_word, simple))
    return pairs


def clean_inline(text: str) -> str:
    text = re.sub(r"`[^`]*`", "CODE", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"(\*\*|__|\*|_)(?=\S)(.+?)(?<=\S)\1", r"\2", text)
    return text.strip()


def drop_quotes(sentence: str) -> str:
    """Remove quoted spans, so that a mention of a word ("should") is not a use."""
    return re.sub(r'"[^"]*"|\u201c[^\u201d]*\u201d', " ", sentence)


def split_sentences(text: str) -> list[str]:
    protected = text
    for abbr in ABBREVIATIONS:
        protected = re.sub(re.escape(abbr), abbr.replace(".", "․"), protected, flags=re.I)
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[A-Z0-9\"'(\[])", protected)
    return [p.replace("․", ".").strip() for p in parts if p.strip()]


def count_words(sentence: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][\w'’\-/.,]*", sentence))


def blocks(lines: list[str]):
    """Yield (start_line, kind, text) for each prose block.

    kind is "step" (numbered item), "item" (bulleted item), "cell" (table
    cell) or "para" (paragraph).
    """
    in_fence = False
    in_front = bool(lines) and lines[0].strip() == "---"
    buf: list[str] = []
    buf_start = 0
    buf_kind = "para"

    def flush():
        nonlocal buf
        if buf:
            yield_value = (buf_start, buf_kind, " ".join(buf))
            buf = []
            return yield_value
        return None

    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        stripped = line.strip()
        if in_front:
            if i > 1 and stripped in ("---", "..."):
                in_front = False
            continue
        if re.match(r"^(```|~~~)", stripped):
            out = flush()
            if out:
                yield out
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped or stripped.startswith(("#", "<!--", "-->")) or re.match(r"^([-*_]\s*){3,}$", stripped):
            out = flush()
            if out:
                yield out
            continue
        if stripped.startswith("|"):
            out = flush()
            if out:
                yield out
            if re.match(r"^\|?[\s:|-]+\|?$", stripped):
                continue
            for cell in stripped.strip("|").split("|"):
                if cell.strip():
                    yield (i, "cell", cell.strip())
            continue
        if stripped.startswith(">"):
            stripped = stripped.lstrip("> ").strip()
            if not stripped:
                continue
        numbered = re.match(r"^\d+[.)]\s+(.*)$", stripped)
        bulleted = re.match(r"^[-*+]\s+(?:\[[ xX]\]\s+)?(.*)$", stripped)
        if numbered or bulleted:
            out = flush()
            if out:
                yield out
            buf = [(numbered or bulleted).group(1)]
            buf_start = i
            buf_kind = "step" if numbered else "item"
            continue
        if not buf:
            buf_start = i
            buf_kind = "para"
        buf.append(stripped)
    out = flush()
    if out:
        yield out


def check_file(path: Path, args, word_list) -> list[Observation]:
    obs: list[Observation] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    name = str(path)
    for start, kind, raw_text in blocks(lines):
        text = clean_inline(raw_text)
        if not text:
            continue
        sentences = split_sentences(text)
        if kind == "para" and len(sentences) > args.para_limit:
            obs.append(Observation(name, start, "PARA",
                                   f"{len(sentences)} sentences in one paragraph (limit {args.para_limit})",
                                   sentences[0][:80]))
        for s in sentences:
            words = count_words(s)
            is_rule = kind == "step" or bool(RULE_WORDS.search(s))
            limit = args.rule_limit if is_rule else args.desc_limit
            label = "rule/step" if is_rule else "description"
            excerpt = s if len(s) <= 120 else s[:117] + "..."
            used = drop_quotes(s)
            if words > limit:
                obs.append(Observation(name, start, "LEN", f"{words} words, {label} limit {limit}", excerpt))
            for m in MODALS.finditer(used):
                obs.append(Observation(name, start, "MODAL",
                                       f'"{m.group(0)}": in a rule use must / can / cannot', excerpt))
            for m in FUTURE.finditer(used):
                obs.append(Observation(name, start, "FUTURE", f'"{m.group(0)}": use the present tense', excerpt))
            for m in PASSIVE.finditer(s):
                if m.group(1).lower() in NOT_PARTICIPLES:
                    continue
                obs.append(Observation(name, start, "PASSIVE",
                                       f'"{m.group(0)}": name the actor, if it is known', excerpt))
            for m in NOMINAL.finditer(used):
                obs.append(Observation(name, start, "NOUN", f'"{m.group(0)}": use the verb', excerpt))
            cond = LATE_CONDITION.search(used)
            before = used[:cond.start()].split() if cond else []
            if cond and before and before[-1].lower() not in ("even", "only", "as", "what"):
                obs.append(Observation(name, start, "COND",
                                       f'"{cond.group(0)}" after the start: put the condition first', excerpt))
            if SEMICOLON.search(s.rstrip(";").rstrip() if kind in ("item", "step") else s):
                obs.append(Observation(name, start, "SEMI", "semicolon: use a list or two sentences", excerpt))
            for pattern, complex_word, simple in word_list:
                if pattern.search(used):
                    obs.append(Observation(name, start, "WORD", f'"{complex_word}" -> "{simple}"', excerpt))
    return obs


def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(f for f in path.rglob("*") if f.suffix.lower() in (".md", ".markdown", ".txt")))
        elif path.exists():
            files.append(path)
        else:
            print(f"ste_check: cannot read {p}", file=sys.stderr)
            sys.exit(2)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--rule-limit", type=int, default=20, help="word limit for a rule or a step (default 20)")
    ap.add_argument("--desc-limit", type=int, default=25, help="word limit for a description (default 25)")
    ap.add_argument("--para-limit", type=int, default=6, help="sentence limit for a paragraph (default 6)")
    ap.add_argument("--json", action="store_true", help="print observations as JSON")
    ap.add_argument("--summary", action="store_true", help="print the counts only")
    args = ap.parse_args()

    word_list = load_word_list(WORD_LIST)
    all_obs: list[Observation] = []
    for f in collect(args.paths):
        all_obs.extend(check_file(f, args, word_list))

    counts: dict[str, int] = {}
    for o in all_obs:
        counts[o.code] = counts.get(o.code, 0) + 1

    if args.json:
        print(json.dumps({"counts": counts, "total": len(all_obs),
                          "observations": [asdict(o) for o in all_obs]}, indent=2))
        return 0
    if not args.summary:
        for o in all_obs:
            print(f"{o.file}:{o.line} {o.code} {o.message} | {o.excerpt}")
    summary = ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "none"
    print(f"\n{len(all_obs)} observations: {summary}")
    print("Observations, not verdicts: check each one against the meaning of the text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
