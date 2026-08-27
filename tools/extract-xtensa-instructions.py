#!/usr/bin/env python3
"""Extract the complete assembler-visible instruction-name set from Espressif's
pinned xtensa-isa-doc checkout.

Usage:
    git clone https://github.com/espressif/xtensa-isa-doc
    cd xtensa-isa-doc
    git checkout 00216044559526727d058feffc8fd09957d96b19
    python /path/to/extract-xtensa-instructions.py .

The output is TSV: mnemonic, source file.  It is deliberately an architecture
inventory, not an Idriç support list.  Per-chip optional-instruction filtering
must then be applied using the matching ESP-IDF core-isa.h configuration.
"""

from pathlib import Path
import re
import sys

PIN = "00216044559526727d058feffc8fd09957d96b19"
ROW = re.compile(r"^\s*([A-Z][A-Z0-9_.]*)\s*&\s*[^&]*\\\\\s*(?:\\hline)?\s*$")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: extract-xtensa-instructions.py XTENSA_ISA_DOC_CHECKOUT", file=sys.stderr)
        return 2

    root = Path(sys.argv[1])
    files = sorted(root.glob("Instructions*.tex"))
    # Code-density instructions have historically lived outside Instructions*.tex.
    for name in ("CodeDensity.tex", "WindowedOption.tex"):
        p = root / name
        if p.exists():
            files.append(p)

    found: dict[str, set[str]] = {}
    for path in files:
        for line in path.read_text(encoding="utf-8").splitlines():
            m = ROW.match(line)
            if not m:
                continue
            found.setdefault(m.group(1), set()).add(path.name)

    if not found:
        print("no instruction rows found; wrong checkout/layout?", file=sys.stderr)
        return 1

    print(f"# xtensa-isa-doc pin\t{PIN}")
    print("mnemonic\tsource")
    for mnemonic in sorted(found):
        print(f"{mnemonic}\t{','.join(sorted(found[mnemonic]))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
