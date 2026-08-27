#!/usr/bin/env python3
"""Snapshot and index the complete pinned WGSL/WebGPU spec surface.

The canonical files are always written verbatim first. Normalized indexes are
convenience views; they are never allowed to replace the canonical snapshots.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.request

PIN = "7af79e816d5ae53626cb28b79be1fe83bb63c871"
BASE = f"https://raw.githubusercontent.com/gpuweb/gpuweb/{PIN}/"
FILES = {
    "wgsl-syntax.bnf": "wgsl/syntax.bnf",
    "wgsl-index.bs": "wgsl/index.bs",
    "webgpu-index.bs": "spec/index.bs",
}

PRODUCTION = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*$")
LITERAL = re.compile(r"'([^'\\]*(?:\\.[^'\\]*)*)'")
IDL_BLOCK = re.compile(r"<pre[^>]*class=[\"']idl[\"'][^>]*>(.*?)</pre>", re.S | re.I)
IDL_DECL = re.compile(
    r"^\s*(interface(?:\s+mixin)?|dictionary|enum|typedef|callback|namespace)\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.M,
)
DFN = re.compile(r"<dfn\b([^>]*)>(.*?)</dfn>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")
FEATURE = re.compile(r"\b(?:enable|requires)\s+([A-Za-z_][A-Za-z0-9_]*)")


def fetch(path: str) -> bytes:
    with urllib.request.urlopen(BASE + path) as r:
        return r.read()


def clean_html(text: str) -> str:
    return " ".join(TAG.sub("", text).replace("&lt;", "<").replace("&gt;", ">").split())


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "surface")
    out.mkdir(parents=True, exist_ok=True)

    manifest = {"repository": "gpuweb/gpuweb", "commit": PIN, "files": {}}
    decoded: dict[str, str] = {}

    for local, remote in FILES.items():
        data = fetch(remote)
        (out / local).write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        manifest["files"][local] = {
            "source": BASE + remote,
            "sha256": digest,
            "bytes": len(data),
        }
        decoded[local] = data.decode("utf-8")

    grammar = decoded["wgsl-syntax.bnf"]
    productions = [m.group(1) for m in PRODUCTION.finditer(grammar)]
    literals = sorted(set(m.group(1) for m in LITERAL.finditer(grammar)))
    (out / "wgsl-grammar-productions.txt").write_text("\n".join(productions) + "\n", encoding="utf-8")
    (out / "wgsl-literals.txt").write_text("\n".join(literals) + "\n", encoding="utf-8")

    wgsl = decoded["wgsl-index.bs"]
    dfns = []
    for m in DFN.finditer(wgsl):
        name = clean_html(m.group(2))
        if name:
            dfns.append(name)
    (out / "wgsl-definitions.txt").write_text("\n".join(sorted(set(dfns))) + "\n", encoding="utf-8")
    features = sorted(set(FEATURE.findall(wgsl)))
    (out / "wgsl-feature-names.txt").write_text("\n".join(features) + "\n", encoding="utf-8")

    webgpu = decoded["webgpu-index.bs"]
    blocks = IDL_BLOCK.findall(webgpu)
    (out / "webgpu-webidl.txt").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    decls = []
    for block in blocks:
        decls.extend(f"{kind}\t{name}" for kind, name in IDL_DECL.findall(clean_html(block)))
    (out / "webgpu-idl-declarations.tsv").write_text("kind\tname\n" + "\n".join(sorted(set(decls))) + "\n", encoding="utf-8")

    manifest["normalized"] = {
        "wgsl_grammar_productions": len(productions),
        "wgsl_literal_tokens": len(literals),
        "wgsl_definitions": len(set(dfns)),
        "wgsl_feature_names": len(features),
        "webgpu_idl_blocks": len(blocks),
        "webgpu_idl_declarations": len(set(decls)),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not productions or not blocks:
        raise SystemExit("normalization failed: expected WGSL productions and WebGPU WebIDL blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
