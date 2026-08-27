# WGSL / WebGPU complete surface inventory

Status: exhaustive source-backed language/API inventory, independent of the small Idriç compute-shader subset.

WebGPU is not a machine ISA, and WGSL is not native GPU bytecode. The analogue of a complete instruction inventory is therefore the complete **WGSL language surface** plus the complete **WebGPU API/command/resource surface**.

## Canonical source pin

Repository: `gpuweb/gpuweb`

Commit: `7af79e816d5ae53626cb28b79be1fe83bb63c871`

Canonical files at that immutable revision:

- `wgsl/syntax.bnf` — complete WGSL grammar;
- `wgsl/index.bs` — complete WGSL specification, including types, address spaces, attributes, operators, built-ins, stage interfaces, memory model, feature requirements and semantics;
- `spec/index.bs` plus `spec/sections/` — complete WebGPU specification source, including WebIDL interfaces/dictionaries/enums, resource objects, pipelines, encoders/passes, commands, queue operations, validation and feature/limit surfaces.

The pinned file hashes at this revision are:

- `wgsl/syntax.bnf`: `423ecb96a4b4473f9c8de3615eb2582fa5f452d7`
- `wgsl/index.bs`: `fde6e0d4fe612dc929f6f061c50f812a82da0457`
- `spec/index.bs`: `db77e22e83e3689699f4049f7126de43a35c4a13`

## What "complete" means here

The WGSL inventory must retain all of the following, not merely the subset used by an initial compute shader:

- every grammar production and token class;
- all scalar, vector, matrix, array, structure, pointer, atomic, sampler and texture types;
- all address spaces and access modes;
- all module directives and declarations;
- all attributes and their arguments;
- all expressions and operators;
- all statements and structured control-flow forms;
- all constructors and conversions;
- every built-in function overload family;
- every built-in value and stage interface;
- compute, vertex and fragment stages;
- derivatives, texture operations, atomics, barriers, packing/unpacking, subgroup and quad operations where present in the pinned spec;
- every standardized/enabled language extension and feature requirement;
- memory, synchronization and execution semantics.

The WebGPU inventory must retain:

- every WebIDL interface, dictionary, enum, typedef and callback in the pinned specification;
- adapter/device/queue operations;
- buffers, textures, texture views, samplers and external textures;
- bind groups/layouts and pipeline layouts;
- shader modules and compilation information;
- compute/render pipeline creation;
- command encoders and command buffers;
- compute/render pass encoders and every encoded command;
- copies, clears, resolves and query operations;
- canvas/presentation configuration;
- error scopes, device-loss/error objects, features and limits;
- synchronization/queue submission and mapping behavior.

## Reproducible inventory

`tools/generate-surface.py` fetches only the immutable revision above and writes a local inventory directory containing the complete canonical source files plus normalized indexes for:

1. WGSL grammar productions and literal keywords/operators;
2. WGSL Bikeshed definitions and feature/extension declarations;
3. WebGPU WebIDL blocks and their interfaces/dictionaries/enums/members;
4. a manifest with SHA-256 hashes and source URLs.

The verbatim pinned source files are part of the generated result so a normalization bug cannot silently erase part of the language/API while still claiming completeness.

## Idriç support is separate

`ARCHITECTURE.md` intentionally describes a much smaller first compute-shader slice. That file is an implementation plan, not the language inventory. Unsupported WGSL/WebGPU operations remain in the complete source-backed inventory.

Native GPU ISAs such as NVIDIA Maxwell/Ampere or AMD RDNA are separate architectures. They require separate native instruction inventories if Idriç ever targets them directly.
