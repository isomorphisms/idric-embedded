# Idriç Steam target

This branch treats Steam as a **platform target**, not as a new processor architecture or shader backend.

## Ownership

Compiler work is now deliberately split by layer:

- **CPU / x86-64**: [`isomorphisms/idric-x86-aggressive-backend`](https://github.com/isomorphisms/idric-x86-aggressive-backend).
- **Steam Deck GPU / RDNA2 + Vulkan/SPIR-V**: [`isomorphisms/idris-shader-backend:target/steam-rdna2-vulkan`](https://github.com/isomorphisms/idris-shader-backend/tree/target/steam-rdna2-vulkan).
- **This branch**: SteamOS/Steam Linux Runtime, executable deployment, window/presentation/input/audio/filesystem/Steam integration, and the connection between host code and the shader backend.

Do not maintain a second Vulkan GLSL/SPIR-V emitter here. The shader repository is the single compiler-facing home.

## Layers

```text
Idriç host program
    ↓
x86-64 code generation
    ↓
Linux executable + process ABI
    ↓
Steam Linux Runtime / SteamOS
    ↓
window, input, audio, filesystem, presentation

Idriç shader subset
    ↓
idris-shader-backend target/steam-rdna2-vulkan
    ↓
Vulkan GLSL → SPIR-V
    ↓
Vulkan driver
    ↓
Steam Deck RDNA2 GPU
```

These layers should stay separate.

- **CPU ISA**: x86-64 / AMD64.
- **calling convention and executable ABI**: arguments, returns, registers, stack, ELF, dynamic linking and process startup.
- **Steam Linux Runtime / SteamOS**: deployment/runtime environment, not the compiler backend.
- **shader compiler**: shared shader IR plus Vulkan GLSL/SPIR-V lowering in the shader repository.
- **graphics API**: Vulkan resource, pipeline and command submission.
- **GPU ISA**: RDNA2 machine code, separately documented in the shader target branch.
- **Steam platform APIs**: controller/input, Steamworks and related services remain platform work rather than shader semantics.

## First concrete deployment boundary

For a first reproducible Steam target, prefer:

1. native **x86-64 Linux** rather than solving Windows/Proton and native Linux simultaneously;
2. the existing x86-64 backend as owner of CPU code generation;
3. an ordinary ELF executable with a deliberately small Linux ABI surface;
4. the current Steam Linux Runtime as deployment environment;
5. generated Vulkan/SPIR-V shader work from `target/steam-rdna2-vulkan`;
6. one deterministic frame and one controller/keyboard input as the first visible platform proof;
7. Steamworks-specific features only after ordinary launch, rendering, input and exit work.

The CPU oracle and GPU oracle remain independently testable. A host program should still be provable without Vulkan, and a generated shader should still be compilable/validated without requiring Steam distribution machinery.

## GPU target precision

The shader branch is pinned to the Steam Deck's AMD RDNA2 GPU rather than treating every machine running Steam as one GPU architecture. A future Steam machine with a materially different GPU should either use another existing shader target or get its own target branch. “Steam” itself is never the GPU ISA.

## Related

- centralized Steam Deck shader target: [`idris-shader-backend/target/steam-rdna2-vulkan`](https://github.com/isomorphisms/idris-shader-backend/tree/target/steam-rdna2-vulkan)
- CPU backend: [`idric-x86-aggressive-backend`](https://github.com/isomorphisms/idric-x86-aggressive-backend)
- compiler/language: [`Idric`](https://github.com/isomorphisms/Idric)
- Steam deployment issue: [#6](https://github.com/isomorphisms/idric-embedded/issues/6)
- Valve Steam Runtime reference: <https://github.com/ValveSoftware/steam-runtime>
- Steam Deck hardware reference: <https://www.steamdeck.com/en/tech>

## Scope rule

Keep this branch even though it owns neither CPU nor shader instruction selection. Its job is:

> Given correct Idriç-generated x86-64 host code and correct generated Vulkan/SPIR-V shader code, what additional contracts are required to turn them into a reproducibly runnable Steam program?
