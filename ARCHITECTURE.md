# WebGPU / WGSL architecture notes

Status: 2026-08-27

## Classification

**WebGPU is not an instruction set.** It is a portable GPU API and command model. The browser or native implementation maps its resources, pipelines and command buffers onto the platform's native graphics stack.

The closest compiler target is **WGSL**, the WebGPU Shading Language. WGSL is also not a hardware ISA or portable GPU bytecode: it is a typed shader language supplied as source to `GPUShaderModule`, then compiled by the implementation for the actual GPU backend.

Pin the standards boundary to the current 2026 W3C documents while also recording the live editor drafts:

- WebGPU W3C Candidate Recommendation Draft: https://www.w3.org/TR/webgpu/
- WGSL W3C Candidate Recommendation Draft: https://www.w3.org/TR/WGSL/
- WebGPU editor draft: https://gpuweb.github.io/gpuweb/
- WGSL editor draft: https://gpuweb.github.io/gpuweb/wgsl/

## Two distinct compiler boundaries

Do not collapse host code and GPU shader code into one backend.

A useful model is:

`Idriç host code -> Wasm/native host backend -> WebGPU API`

and separately:

`Idriç shader subset -> WGSL -> WebGPU implementation -> native GPU representation/ISA`

The `webgpu` branch should primarily investigate the second arrow plus the minimal host API required to prove it executes.

## WebGPU execution model

The host side exposes objects such as:

- adapter/device/queue;
- buffers and textures;
- bind groups and pipeline layouts;
- shader modules;
- compute and render pipelines;
- command encoders and command buffers;
- compute/render passes;
- copies and queries.

Work reaches the GPU through encoded draw or dispatch commands. WebGPU has two pipeline classes:

- compute pipeline;
- render pipeline.

WGSL provides three programmable shader stages:

- compute;
- vertex;
- fragment.

## WGSL language surface

Important scalar types include:

- `bool`;
- `i32`;
- `u32`;
- `f32`;
- optional `f16` when the `shader-f16` feature is available.

WGSL also provides vectors, matrices, arrays, structures, pointers/references to permitted address spaces, atomics, textures and samplers.

The language is structured and imperative. Its executable surface includes declarations, assignments, expressions and structured control such as:

- `if` / `else`;
- `switch`;
- `loop`;
- `while`;
- `for`;
- `break` / `continue`;
- `return`;
- stage-specific termination such as fragment `discard`.

Major built-in-operation families include:

- constructors and conversions;
- bit reinterpretation;
- logical operations;
- array operations;
- scalar/vector/matrix numeric operations;
- derivatives;
- texture sampling/loading/storing;
- atomics;
- packing/unpacking;
- synchronization/barriers;
- subgroup operations;
- quad operations.

Those built-ins are a much better architecture inventory for an Idriç shader backend than pretending WebGPU has opcodes.

## Memory and parallelism

The compiler must preserve WGSL's explicit execution/memory model rather than import CPU assumptions.

Important concepts include:

- shader invocations;
- workgroups for compute shaders;
- storage/uniform resources supplied through bindings;
- private/function/workgroup storage;
- explicit workgroup/storage synchronization where permitted;
- subgroup and quad operations as later optional facilities.

Compute shaders expose a particularly clean first target because inputs and outputs can live entirely in bound buffers.

## First Idriç executable surface

Start with **compute only**.

The first generated WGSL slice should need only:

1. `u32`, `i32`, and `f32` scalar values;
2. small vectors only when a fixture needs them;
3. `let`/`var`, function parameters and local expressions;
4. arithmetic, comparison and boolean expressions;
5. `if` and a simple loop if required;
6. one `@compute` entry point with a fixed `@workgroup_size`;
7. `@builtin(global_invocation_id)`;
8. one or two `var<storage>` bound buffers;
9. indexed storage-buffer loads and stores.

The first oracle should be deterministic and embarrassingly small, for example:

`out[i] = in[i] + 1`

or a two-buffer vector addition. The host creates buffers, creates the shader module and compute pipeline, dispatches a known number of invocations, copies/readbacks the result, and compares exact values.

Keep these outside the first slice:

- render pipelines;
- vertex/fragment stages;
- textures/samplers;
- derivatives;
- atomics;
- barriers beyond what the first independent-invocation kernel needs;
- subgroups and quad operations;
- optional `f16` until feature negotiation is explicit;
- implementation-specific native shader representations.

## Why this belongs next to Wasm

The two branches are complementary rather than competing architectures. A browser application can plausibly use a small Wasm module for host-side Idriç code while sending compiler-generated WGSL kernels through WebGPU.

That keeps the device-independent program boundary intact: CPU-like logic targets Wasm; explicitly parallel graphics/compute kernels target WGSL; WebGPU remains the runtime/device API joining the shader to real hardware.