#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from wasmtime import Engine, Instance, Module, Store


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("module", type=Path)
    parser.add_argument("--export", default="idric_answer")
    parser.add_argument("--expect", type=int, default=42)
    args = parser.parse_args()

    engine = Engine()
    module = Module.from_file(engine, str(args.module))

    if module.imports:
        names = [f"{item.module}.{item.name}" for item in module.imports]
        raise AssertionError(f"first Wasm slice must have zero imports, got {names}")

    store = Store(engine)
    instance = Instance(store, module, [])
    exported = instance.exports(store)
    function = exported[args.export]
    result = function(store)
    if result != args.expect:
        raise AssertionError(f"{args.export}() returned {result}, expected {args.expect}")


if __name__ == "__main__":
    main()
