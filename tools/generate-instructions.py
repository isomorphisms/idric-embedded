#!/usr/bin/env python3
"""Emit every WebAssembly Core instruction-table row from the pinned spec.

The upstream source is parsed as Python AST but never executed.
Output is TSV in official source order, including reserved opcode rows.
"""

from __future__ import annotations

import ast
import csv
import io
import sys
import urllib.request

COMMIT = "4b29bdbced924599346ea2ffd9e975af5d28c735"
URL = (
    "https://raw.githubusercontent.com/WebAssembly/spec/"
    + COMMIT
    + "/document/core/appendix/index-instructions.py"
)
FIELDS = [
    "version",
    "name",
    "opcode",
    "type",
    "validation",
    "execution",
    "operator",
    "validation2",
    "execution2",
]


def literal(node: ast.AST | None):
    if node is None:
        return None
    return ast.literal_eval(node)


def main() -> int:
    with urllib.request.urlopen(URL) as response:
        source = response.read().decode("utf-8")

    tree = ast.parse(source, filename=URL)
    rows = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "INSTRUCTIONS" for t in node.targets):
            continue
        if not isinstance(node.value, ast.List):
            raise SystemExit("INSTRUCTIONS exists but is not a list")

        for i, item in enumerate(node.value.elts):
            if not (
                isinstance(item, ast.Call)
                and isinstance(item.func, ast.Name)
                and item.func.id == "Instruction"
            ):
                raise SystemExit(f"unexpected INSTRUCTIONS entry {i}: {ast.dump(item)}")

            values = {field: None for field in FIELDS}
            for field, arg in zip(FIELDS, item.args):
                values[field] = literal(arg)
            for kw in item.keywords:
                if kw.arg not in values:
                    raise SystemExit(f"unknown Instruction keyword: {kw.arg}")
                values[kw.arg] = literal(kw.value)
            rows.append(values)
        break
    else:
        raise SystemExit("INSTRUCTIONS table not found")

    if not rows:
        raise SystemExit("empty instruction table")

    out = csv.writer(sys.stdout, dialect="excel-tab", lineterminator="\n")
    out.writerow(["index", *FIELDS])
    for i, values in enumerate(rows):
        out.writerow([i, *("" if values[f] is None else values[f] for f in FIELDS)])

    print(f"# source={URL}", file=sys.stderr)
    print(f"# rows={len(rows)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
