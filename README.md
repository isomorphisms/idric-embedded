# Idriç Nintendo Switch target

This branch treats Nintendo Switch as a **platform target built on 64-bit Arm**, not as a new instruction set invented by Nintendo.

It is worth keeping a `switch` branch anyway because reaching a console requires much more than emitting instructions for its CPU.

## CPU boundary

The original Nintendo Switch family uses NVIDIA Tegra X1/X1+ hardware with 64-bit Arm Cortex-A57/A53 CPU cores. Nintendo Switch 2 uses a different NVIDIA SoC, publicly identified as T239, with 64-bit Arm Cortex-A78C cores. Both therefore belong to the **AArch64 / 64-bit Arm** side of the compiler architecture map, although the exact architectural extensions, microarchitecture, platform ABI, graphics hardware, and deployment environment differ by generation.

This is an important distinction from the existing [`isomorphisms/idric-arm-thumb`](https://github.com/isomorphisms/idric-arm-thumb) work. Thumb/Thumb-2 is a 32-bit Arm instruction encoding and execution target. A Switch executable should not be described as a Thumb target merely because both processors are Arm.

There is not currently a dedicated Idriç AArch64 backend repository. Until one is created or designated, the relevant references are:

- compiler/language: [`isomorphisms/Idric`](https://github.com/isomorphisms/Idric)
- existing Arm backend patterns, **reference only for Switch code generation**: [`isomorphisms/idric-arm-thumb`](https://github.com/isomorphisms/idric-arm-thumb)

If Switch work advances beyond research, the CPU work should get an explicitly AArch64 owner rather than quietly extending a repository whose contract says Thumb.

## Layers

A useful way to read the target is:

```text
Idriç program
    ↓
AArch64 code generation
    ↓
Switch executable + platform ABI
    ↓
Nintendo OS/runtime or public homebrew runtime
    ↓
controller, display, audio, filesystem, timing, graphics APIs
    ↓
Arm CPU + NVIDIA GPU hardware
```

Again, these are different contracts.

- **ISA**: AArch64 instructions executed by the Arm CPU.
- **ABI**: register use, stack layout, calls, returns, object/executable format, startup, and the rules for crossing into platform code.
- **platform runtime**: the operating-system and library services available to the program.
- **graphics API**: how the program submits rendering work. This is not the same thing as either the Arm CPU ISA or the NVIDIA GPU's native machine instruction set.
- **distribution**: getting software onto a development/homebrew device is a different problem from publishing a retail Nintendo title.

That decomposition matters for computer science because the same mathematical program may survive unchanged while every layer below it changes. The CPU backend can be shared by unrelated AArch64 devices; a Switch platform layer can change without changing integer addition; and a shader representation can remain device-independent while different drivers ultimately execute very different GPU machine code.

## Switch generations

Do not collapse all hardware sold under the Switch name into one microarchitecture.

### Original Switch / Lite / OLED generation

The relevant public hardware lineage is Tegra X1/X1+, with 64-bit Arm Cortex-A57/A53 CPU cores and NVIDIA Maxwell graphics. The first compiler question is therefore AArch64, not Thumb.

### Switch 2

The public hardware lineage is the NVIDIA T239, with eight 64-bit Arm Cortex-A78C cores and NVIDIA Ampere-family graphics. It is still an AArch64 compiler target, but it should be pinned as a separate hardware/platform generation when instruction extensions, ABI details, GPU behavior, or deployment tooling matter.

The branch can cover both generations conceptually, but every executable test should name the exact generation it is proving.

## Public versus official deployment paths

There are two very different acceptance questions:

1. **Public/reproducible research path** — use public documentation and an openly reproducible homebrew toolchain/runtime where legally appropriate. [`switchbrew/libnx`](https://github.com/switchbrew/libnx) is a useful public reference for the original Switch platform boundary.
2. **Official retail path** — Nintendo's developer program, SDK, signing, certification, packaging, and publishing process are separate access-controlled constraints. Do not infer those interfaces from the CPU ISA and do not make them prerequisites for proving that Idriç can generate correct AArch64 code.

The first backend oracle should therefore be deliberately smaller than "ship a Nintendo game": generate a tiny AArch64 program, execute it through a pinned reproducible environment, and observe a deterministic result. Then add framebuffer/graphics and controller input as separate platform proofs.

## Graphics

The CPU and GPU tracks should remain separate. The original Switch has Maxwell-family NVIDIA graphics; Switch 2 has Ampere-family graphics. That does **not** mean the Idriç CPU compiler should learn Maxwell or Ampere machine instructions.

Existing mathematical shader work lives in [`isomorphisms/idris-shader-backend`](https://github.com/isomorphisms/idris-shader-backend). It currently emits GLSL ES 3.00, so it is useful source/IR work and a reference for preserving the mathematics, but not yet a finished Switch graphics path.

## Related

- Switch deployment issue in this repository: [#5](https://github.com/isomorphisms/idric-embedded/issues/5)
- Steam platform branch: [`steam`](https://github.com/isomorphisms/idric-embedded/tree/steam)
- Existing Arm/Thumb backend: [`idric-arm-thumb`](https://github.com/isomorphisms/idric-arm-thumb)
- Core compiler: [`Idric`](https://github.com/isomorphisms/Idric)
- Public Tegra X1 reference: <https://switchbrew.org/wiki/Tegra_X1>
- Public Switch 2 T239 reference: <https://switchbrew.org/wiki/Switch_2:Tegra_T239>

## Scope rule

Keep this branch even after AArch64 code generation has a proper home. Its question is:

> Given correct Idriç-generated AArch64 code, what additional platform contracts are required to turn it into a reproducibly runnable Nintendo Switch program?

That question is different from "what instructions does an Arm processor implement?", and keeping the two separate should prevent the architecture work from being distorted by console-specific packaging or APIs.
