# WebAssembly architecture notes

Status: 2026-08-27

## Classification

WebAssembly is a real virtual instruction-set architecture rather than a physical processor ISA. The core specification defines module structure, types, instructions, binary/text encodings, validation, instantiation, and execution semantics independently of any particular host environment.

Pin the architecture inventory to **WebAssembly Core Specification 3.0, released 2026-08-26**.

Primary references:

- Core 3.0: https://webassembly.github.io/spec/core/
- instruction index: https://webassembly.github.io/spec/core/appendix/index-instructions.html
- 3.0 change history: https://webassembly.github.io/spec/core/appendix/changes.html
- TinyGo WebAssembly guide, as an implementation comparison rather than an Idriç design constraint: https://tinygo.org/docs/guides/webassembly/

## Execution model

WebAssembly is a typed stack machine. Execution uses an operand/control stack plus an abstract store. Control flow is structured rather than an arbitrary native-PC branch graph.

Core numeric value types are:

- `i32`
- `i64`
- `f32`
- `f64`

The core also has `v128` plus reference/heap types. There is **no scalar `f16` core number type** in WebAssembly 3.0.

The main instruction families are:

- structured control: `block`, `loop`, `if`, branches, return, calls, tail calls, exception control;
- parametric stack operations: `drop`, `select`;
- locals and globals;
- tables and references;
- linear-memory load/store, size/grow and bulk-memory operations;
- scalar integer and floating arithmetic, comparisons, bit operations and conversions;
- `v128` SIMD operations;
- typed-reference and GC operations for references, structs and arrays.

Binary instructions are opcode encoded with immediate operands where required. WebAssembly 3.0 retains the explicit validation rules that type each instruction by what it consumes from and produces onto the operand stack.

## What changed by Core 3.0

The complete architecture inventory now includes facilities well beyond the old MVP, including:

- extended constant expressions;
- tail calls;
- exception handling;
- multiple memories;
- 64-bit memory/table address spaces (`memory64`);
- typed/function references;
- managed GC reference, struct and array types;
- relaxed SIMD;
- deterministic profiles.

These belong in the architecture inventory. They do **not** belong automatically in the first compiler-generated subset.

## Embedding is not the ISA

Keep the core ISA separate from its host interface.

Potential host boundaries include:

- browser/JavaScript WebAssembly embedding;
- WASI Preview 1 or Preview 2;
- native runtimes such as Wasmtime-style embedders.

The first compiler proof does not need to choose a large runtime ABI. A pure core module can export a function and let a tiny host call it and check the return value.

## First Idriç executable surface

Start deliberately closer to a `wasm32` scalar profile even though the architecture inventory records all of Core 3.0:

1. module/type/function/code/export sections;
2. `i32` constants and function parameters/results;
3. `local.get`, `local.set`, `local.tee`;
4. integer arithmetic and logic: add/sub/mul and basic bit operations;
5. comparisons and `eqz`;
6. structured `block`/`loop`/`if`, `br`, `br_if`, `return`;
7. direct `call`;
8. one 32-bit-addressed linear memory;
9. basic `i32.load`/`i32.store` plus byte/halfword forms when required by source types.

The first observable oracle should be an exported generated function returning a known integer. The next should exercise a linear-memory load/store round trip. After that, add branch/call fixtures.

Keep these outside the first slice:

- `f64` unless a source test specifically requires it;
- SIMD/relaxed SIMD;
- GC/reference object lowering;
- exceptions;
- tail calls;
- multiple memories;
- memory64;
- WASI or browser-specific APIs.

## Compiler boundary

The Idriç target-independent IR should not learn that WebAssembly is stack based. Lower ordinary typed operations and control flow into a WebAssembly-specific representation late, then validate the emitted module against the pinned specification.

Complete architecture knowledge and tiny executable code generation are separate deliverables. The backend succeeds first when a small compiler-generated module validates and executes reproducibly, not when every Core 3.0 opcode has a lowering.