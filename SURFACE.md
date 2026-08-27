# WebGPU / WGSL surface handoff

The complete compiler-facing WGSL/WebGPU surface inventory has moved to the shader repository:

- [`isomorphisms/idris-shader-backend:target/webgpu-wgsl`](https://github.com/isomorphisms/idris-shader-backend/tree/target/webgpu-wgsl)
- flat inventory: [`targets/webgpu-wgsl/SURFACE.txt`](https://github.com/isomorphisms/idris-shader-backend/blob/target/webgpu-wgsl/targets/webgpu-wgsl/SURFACE.txt)
- WGSL families: [`families/wgsl-language.md`](https://github.com/isomorphisms/idris-shader-backend/blob/target/webgpu-wgsl/targets/webgpu-wgsl/families/wgsl-language.md)
- WebGPU API families: [`families/webgpu-api.md`](https://github.com/isomorphisms/idris-shader-backend/blob/target/webgpu-wgsl/targets/webgpu-wgsl/families/webgpu-api.md)
- memory/execution families: [`families/memory-and-execution.md`](https://github.com/isomorphisms/idris-shader-backend/blob/target/webgpu-wgsl/targets/webgpu-wgsl/families/memory-and-execution.md)
- API completeness extractor: [`tools/extract_webgpu_types.py`](https://github.com/isomorphisms/idris-shader-backend/blob/target/webgpu-wgsl/targets/webgpu-wgsl/tools/extract_webgpu_types.py)

This file intentionally no longer carries a second copy of the WGSL built-ins, WebGPU verbs, feature names, formats or option lists. Keeping two exhaustive inventories would guarantee drift.

The `idric-embedded/webgpu` branch now owns only deployment/runtime questions adjacent to Wasm/embedded host execution. The shader repository is canonical for the language/compiler/API inventory.
