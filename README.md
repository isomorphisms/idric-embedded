# idric-embedded — WebAssembly

This branch is the WebAssembly architecture follower for Idriç. `ARCHITECTURE.md`
pins WebAssembly Core 3.0 and keeps the complete architecture inventory separate
from the first executable backend slice.

## First executable slice

The first implementation deliberately accepts only one shape:

```idris
%export "wasm:idric_answer"
idric_answer : Int32
idric_answer = 42
```

The real `.idric` source goes through the pinned Idriç frontend and
`Compiler.ANF`. The Wasm backend then accepts exactly one exported nullary ANF
function whose reachable body is one `Int32` literal and emits a binary module
containing only:

- one function type: `() -> i32`
- one function at type index 0
- one function export
- one code body: no locals, `i32.const`, `end`

The binary therefore contains exactly section IDs `1, 3, 7, 10`: type,
function, export, and code. It has no import, table, memory, global, start,
element, data, tag, or custom section.

WebAssembly Core 3.0 still uses binary-format version 1 in the module preamble;
`\0asm 01 00 00 00` is therefore the current Core binary format, not a claim
that this backend targets only Wasm 1.0.

## Verification

```sh
make verify IDRIC=/path/to/Idric/build/exec/idris2
```

The gate pins Idriç commit
`081b9cde0591154839fb5d80d76e5570e0436300` and Wasmtime Python `48.0.0`.
It:

1. typechecks and builds the custom `wasm` code generator;
2. compiles `tests/KnownInteger.idric` to `build/exec/known-integer.wasm`;
3. independently inspects the binary shape and rejects any extra section;
4. asks Wasmtime to parse/validate the binary;
5. requires the module to have zero imports;
6. instantiates it with an empty import list and requires
   `idric_answer() == 42`;
7. recompiles the source twice and requires byte-identical `.wasm` output.

Wasmtime is only the pinned independent validation/execution engine. The
generated module imports nothing and does not depend on JavaScript, browser
APIs, WASI, or any operating-system interface.

## Deliberate boundary

This PR proves only the first oracle from issue #7. It does **not** implement
linear memory, integer arithmetic beyond the literal, locals, comparisons,
structured control flow, direct calls, SIMD, GC/reference objects, exceptions,
tail calls, multiple memories, `memory64`, browser APIs, or WASI.

The next slice should remain inside the issue's initial Core surface and add the
memory store/load round trip before branch and direct-call fixtures.
