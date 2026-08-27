# Idriç Nintendo Switch target

This branch treats Nintendo Switch as a **platform target built on 64-bit Arm**, not as a new instruction set invented by Nintendo.

It is worth keeping a `switch` branch because reaching a console requires much more than emitting instructions for its CPU or GPU.

## Ownership

Compiler work is now deliberately split by layer:

- **CPU / AArch64**: belongs to the AArch64 compiler work, not to `idric-arm-thumb`.
- **Original Switch GPU / Tegra X1 Maxwell**: shader compiler work belongs in [`isomorphisms/idris-shader-backend:target/switch-maxwell-sm53`](https://github.com/isomorphisms/idris-shader-backend/tree/target/switch-maxwell-sm53).
- **This branch**: Switch platform ABI/runtime, executable packaging, controller/display/audio/filesystem integration, homebrew deployment and the eventual connection between host code and the shader backend.

Do not add a second GLSL/UAM/deko3d shader compiler here. Keep the shader repository as the single compiler-facing home.

## CPU boundary

The original Nintendo Switch family uses NVIDIA Tegra X1/X1+ hardware with 64-bit Arm Cortex-A57/A53 CPU cores. Nintendo Switch 2 uses a different NVIDIA SoC, publicly identified as T239, with 64-bit Arm Cortex-A78C cores. Both therefore belong to the **AArch64 / 64-bit Arm** side of the compiler architecture map, although the exact architectural extensions, microarchitecture, platform ABI, graphics hardware, and deployment environment differ by generation.

This is an important distinction from [`isomorphisms/idric-arm-thumb`](https://github.com/isomorphisms/idric-arm-thumb). Thumb/Thumb-2 is a 32-bit Arm instruction encoding and execution target. A Switch executable should not be described as a Thumb target merely because both processors are Arm.

There is not currently a dedicated Idriç AArch64 backend repository. Until one is created or designated, the relevant references are:

- compiler/language: [`isomorphisms/Idric`](https://github.com/isomorphisms/Idric)
- existing Arm backend patterns, **reference only for Switch code generation**: [`isomorphisms/idric-arm-thumb`](https://github.com/isomorphisms/idric-arm-thumb)

If Switch work advances beyond research, the CPU work should get an explicitly AArch64 owner rather than quietly extending a repository whose contract says Thumb.

## Layers

```text
Idriç host program
    ↓
AArch64 code generation
    ↓
Switch executable + platform ABI
    ↓
Nintendo OS/runtime or public homebrew runtime
    ↓
controller, display, audio, filesystem, timing, graphics submission

Idriç shader subset
    ↓
idris-shader-backend target/switch-maxwell-sm53
    ↓
UAM-compatible GLSL → DKSH / Maxwell code
    ↓
deko3d
    ↓
Tegra X1 Maxwell GPU
```

These are different contracts.

- **CPU ISA**: AArch64 instructions executed by the Arm CPU.
- **ABI**: register use, stack layout, calls, returns, object/executable format, startup, and the rules for crossing into platform code.
- **platform runtime**: operating-system and library services available to the program.
- **shader compiler**: shared shader IR plus target-specific UAM/Maxwell lowering; centralized in the shader repository.
- **graphics API**: deko3d command/resource submission on the public homebrew path.
- **GPU ISA**: Maxwell machine code, separately inventoried in the shader target branch.
- **distribution**: getting software onto a development/homebrew device is a different problem from publishing a retail Nintendo title.

## Switch generations

Do not collapse all hardware sold under the Switch name into one microarchitecture.

### Original Switch / Lite / OLED generation

The target currently charged for GPU work is the Tegra X1/X1+ generation with NVIDIA Maxwell graphics. The shader branch `target/switch-maxwell-sm53` is explicitly for this generation.

### Switch 2

Switch 2 uses T239 and Ampere-family graphics. It remains an AArch64 CPU target but is **not** covered by the Maxwell shader branch. If/when it becomes a real GPU target, give it its own shader target rather than quietly widening the original-Switch branch.

## Public versus official deployment paths

There are two different acceptance questions:

1. **Public/reproducible research path** — use public documentation and an openly reproducible homebrew toolchain/runtime where legally appropriate. [`switchbrew/libnx`](https://github.com/switchbrew/libnx), [`devkitPro/deko3d`](https://github.com/devkitPro/deko3d), and [`devkitPro/uam`](https://github.com/devkitPro/uam) are the useful public boundaries.
2. **Official retail path** — Nintendo's developer program, SDK, signing, certification, packaging, and publishing process are separate access-controlled constraints. Do not infer those interfaces from the CPU/GPU ISA and do not make them prerequisites for proving compiler correctness.

A first platform oracle remains deliberately smaller than "ship a Nintendo game": execute deterministic generated AArch64 host code, then attach one known shader/frame through the public graphics path, then add controller input.

## Related

- centralized original-Switch shader target: [`idris-shader-backend/target/switch-maxwell-sm53`](https://github.com/isomorphisms/idris-shader-backend/tree/target/switch-maxwell-sm53)
- Switch deployment issue: [#5](https://github.com/isomorphisms/idric-embedded/issues/5)
- Steam platform branch: [`steam`](https://github.com/isomorphisms/idric-embedded/tree/steam)
- existing Arm/Thumb backend: [`idric-arm-thumb`](https://github.com/isomorphisms/idric-arm-thumb)
- core compiler: [`Idric`](https://github.com/isomorphisms/Idric)
- public Tegra X1 reference: <https://switchbrew.org/wiki/Tegra_X1>
- public Switch 2 T239 reference: <https://switchbrew.org/wiki/Switch_2:Tegra_T239>

## Scope rule

Keep this branch even after CPU and shader code generation have proper homes. Its question is:

> Given correct Idriç-generated AArch64 host code and a correct generated Switch shader module, what additional platform contracts are required to turn them into a reproducibly runnable Nintendo Switch program?
