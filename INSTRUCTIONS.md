# WebAssembly Core 3.0 complete instruction inventory

Status: exhaustive source-backed architecture inventory, independent of the tiny Idriç backend subset.

## Canonical source

Pin the WebAssembly specification repository at:

- repository: `WebAssembly/spec`
- commit: `4b29bdbced924599346ea2ffd9e975af5d28c735`
- file: `document/core/appendix/index-instructions.py`

That file contains the `INSTRUCTIONS` table used by the specification itself to generate the official **Index of Instructions**. Each entry carries:

- Core version membership;
- instruction spelling/form;
- binary opcode, including prefixed multi-byte opcode spaces;
- stack type;
- validation reference;
- execution reference;
- reserved opcode rows where applicable.

This is the authoritative exhaustive architecture table for the branch. It is deliberately stronger than a manually maintained list of mnemonic families.

`tools/generate-instructions.py` downloads that exact immutable commit, parses every `Instruction(...)` row in the canonical table, and emits a TSV/Markdown-friendly inventory. A change to the pinned Core version requires changing the source commit explicitly and reviewing the resulting diff.

## Core 3.0 instruction families represented in the canonical table

The generated table includes every concrete operation/form in all of these areas:

- structured control, calls, tail calls and exception control;
- parametric stack operations;
- locals and globals;
- table operations;
- scalar linear-memory loads/stores and packed variants;
- memory size/grow and bulk memory;
- numeric constants;
- every `i32`/`i64` comparison, arithmetic, bit and conversion instruction;
- every `f32`/`f64` comparison, arithmetic and conversion instruction;
- reinterpret/sign-extension/conversion instructions;
- reference instructions;
- table bulk operations;
- SIMD `v128` loads/stores, lane operations, splats, shuffles, comparisons, arithmetic, narrowing/widening, dot-product and relaxed-SIMD instructions;
- reference/GC instructions for refs, structs, arrays and casts/tests;
- all other instruction forms standardized into Core 3.0;
- reserved opcode rows in the official binary map.

The family list above is explanatory only. **The generated canonical table is the complete list.**

## Idriç support is separate

The initial Idriç executable slice in `ARCHITECTURE.md` remains intentionally tiny. It must never be used as the architecture inventory. An instruction can be present in Core 3.0 and unsupported by Idriç without disappearing from this file's canonical data source.

## Reproducibility check

A complete inventory run must satisfy all of these:

1. fetch exactly the pinned commit, not `main`;
2. locate the single `INSTRUCTIONS = [...]` table in `index-instructions.py`;
3. emit every `Instruction(...)` entry in source order, including reserved entries;
4. retain the version and binary opcode fields;
5. fail if parsing skips an entry;
6. compare the generated row count and content when the pin changes.

Browser APIs, WASI and host embedding APIs are deliberately outside this **Core ISA** instruction table. They are separate execution-environment contracts, not Wasm opcodes.
