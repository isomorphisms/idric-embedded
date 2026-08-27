#!/usr/bin/env python3
"""Extract every numbered TriCore instruction heading from an Infineon Vol.2 PDF.

The completeness check is internal to the manual: the Chapter-3 instruction
entries in the table of contents must exactly match the numbered headings found
in the instruction-description body.  A mismatch is a hard failure.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
import tempfile

TOC = re.compile(r"^\s*(3\.[1-9]\.[0-9]+)\s+([A-Z][A-Z0-9.]*)\s+\.{2,}\s*[0-9]+\s*$")
BODY = re.compile(r"^\s*(3\.[1-9]\.[0-9]+)\s+([A-Z][A-Z0-9.]*)\s*$")


def key(section: str):
    return tuple(int(x) for x in section.split('.'))


def parse(lines, pattern):
    found = {}
    for line in lines:
        m = pattern.match(line)
        if not m:
            continue
        section, mnemonic = m.groups()
        old = found.get(section)
        if old is not None and old != mnemonic:
            raise SystemExit(f"section {section} has conflicting mnemonics: {old} / {mnemonic}")
        found[section] = mnemonic
    return found


def main() -> int:
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: extract-manual-instructions.py MANUAL.pdf [instructions.tsv]")
    pdf = Path(sys.argv[1])
    output = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("instructions.tsv")

    with tempfile.TemporaryDirectory() as td:
        text = Path(td) / "manual.txt"
        subprocess.run(["pdftotext", "-layout", str(pdf), str(text)], check=True)
        lines = text.read_text(encoding="utf-8", errors="replace").splitlines()

    toc = parse(lines, TOC)
    body = parse(lines, BODY)
    if not toc:
        raise SystemExit("no Chapter-3 instruction entries found in table of contents")
    if not body:
        raise SystemExit("no Chapter-3 instruction headings found in body")

    toc_set = set(toc.items())
    body_set = set(body.items())
    if toc_set != body_set:
        only_toc = sorted(toc_set - body_set, key=lambda x: key(x[0]))
        only_body = sorted(body_set - toc_set, key=lambda x: key(x[0]))
        print("instruction set mismatch between TOC and body", file=sys.stderr)
        for x in only_toc:
            print(f"TOC only:  {x[0]}\t{x[1]}", file=sys.stderr)
        for x in only_body:
            print(f"body only: {x[0]}\t{x[1]}", file=sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        f.write("section\tmnemonic\n")
        for section, mnemonic in sorted(body.items(), key=lambda x: key(x[0])):
            f.write(f"{section}\t{mnemonic}\n")

    groups = {}
    for section in body:
        group = '.'.join(section.split('.')[:2])
        groups[group] = groups.get(group, 0) + 1
    print(f"{len(body)} complete instruction headings -> {output}", file=sys.stderr)
    for group in sorted(groups, key=key):
        print(f"  {group}: {groups[group]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
