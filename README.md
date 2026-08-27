# WebGPU platform handoff

This branch is retained as an `idric-embedded` breadcrumb because WebGPU can be part of a browser/embedded deployment path, but it no longer owns WGSL shader generation or the canonical WebGPU/WGSL surface inventory.

Compiler-facing shader work now lives in:

- [`isomorphisms/idris-shader-backend:target/webgpu-wgsl`](https://github.com/isomorphisms/idris-shader-backend/tree/target/webgpu-wgsl)

That target branch owns:

- WGSL language/operation inventory;
- WebGPU shader/pipeline/resource API inventory;
- WGSL emission from the shared shader IR;
- feature/precision handling including `f16`, subgroups, immediate data and buffer views;
- generated shader validation and compute/render oracles.

This `idric-embedded/webgpu` branch should only retain deployment/runtime questions that genuinely belong beside Wasm and embedded/browser host execution, for example:

```text
Idriç host code → Wasm/native host backend → browser/native runtime → WebGPU API
```

Do not add a second WGSL emitter or copy the full evolving WGSL API inventory back into this repository.
