# Idriç Steam target

This branch treats Steam as a **platform target**, not as a new processor architecture.

The current Valve machines that matter here—the Steam Deck family and the 2026 Steam Machine—use AMD x86-64 CPUs. CPU instruction selection, register allocation, calling-convention lowering, and other x86-64 backend work therefore belong in [`isomorphisms/idric-x86-aggressive-backend`](https://github.com/isomorphisms/idric-x86-aggressive-backend), not in a Steam-specific instruction selector.

The point of keeping a `steam` branch anyway is that **ISA support is only one layer of a deployable program**.

## Layers

A useful way to read the target is:

```text
Idriç program
    ↓
x86-64 code generation
    ↓
Linux executable + process ABI
    ↓
Steam Linux Runtime / SteamOS
    ↓
window, input, audio, filesystem, timing, graphics APIs
    ↓
CPU + GPU hardware
```

These layers should stay separate.

- **ISA**: x86-64 / AMD64. The processor understands machine instructions such as loads, arithmetic, branches, calls, and SIMD instructions.
- **calling convention and executable ABI**: tells generated code how arguments, return values, registers, stack frames, symbols, ELF objects, dynamic linking, and process startup fit together on a 64-bit Linux host.
- **Steam Linux Runtime**: a binary-compatible user-space runtime used to make native Linux games behave predictably across Linux distributions. It is not an instruction set. Valve currently recommends Steam Linux Runtime 4.0 (`steamrt4`) for new native Linux games.
- **SteamOS**: the Linux-based operating environment used by Deck and Steam Machine. It is not the compiler backend either.
- **graphics/input/platform APIs**: Vulkan, controller input, audio, window/fullscreen behavior, filesystem locations, suspend/resume, Steam Input, Steamworks, and similar facilities sit above the CPU ABI.
- **GPU ISA**: RDNA machine code is a separate problem again. An Idriç CPU backend should not grow RDNA instructions merely because the target machine has an AMD GPU.

This separation is useful computer science in its own right: an architecture tells us what the processor can execute; an ABI tells independently compiled code how to cooperate; an operating-system/runtime boundary tells the executable what services exist; and a graphics API lets programs ask a driver to use hardware whose native instruction set may be entirely different.

## First concrete deployment boundary

For a first reproducible Steam target, prefer:

1. native **x86-64 Linux** rather than trying to solve Windows/Proton and native Linux simultaneously;
2. the existing x86-64 backend as the owner of CPU code generation;
3. an ordinary ELF executable with a deliberately small Linux ABI surface;
4. the current Steam Linux Runtime as the deployment environment;
5. one deterministic frame and one controller/keyboard input as the first visible platform proof;
6. Steamworks-specific features only after ordinary launch, rendering, input, and exit work.

A useful first oracle is therefore not "use Steam." It is: **compile one Idriç function through the x86-64 backend, link it into a minimal native Linux executable, run it under the pinned Steam runtime, and observe a deterministic result.** Then add graphics and input without changing the CPU backend contract.

## Related repositories and notes

- CPU backend: [`isomorphisms/idric-x86-aggressive-backend`](https://github.com/isomorphisms/idric-x86-aggressive-backend)
- Compiler/language: [`isomorphisms/Idric`](https://github.com/isomorphisms/Idric)
- Existing numerical shader work: [`isomorphisms/idris-shader-backend`](https://github.com/isomorphisms/idris-shader-backend). It currently emits GLSL ES 3.00, so it is conceptual/reusable shader work rather than an already-finished Vulkan/SPIR-V Steam path.
- Steam deployment issue in this repository: [#6](https://github.com/isomorphisms/idric-embedded/issues/6)
- Valve Steam Runtime reference: <https://github.com/ValveSoftware/steam-runtime>
- Steam Deck hardware reference: <https://www.steamdeck.com/en/tech>

## Scope rule

Keep this branch even though it does not own a new CPU ISA. Its job is to answer a different question:

> Given that Idriç can already produce code for the host processor, what additional contracts are required to turn that code into a reproducibly runnable Steam game?

That same distinction should be reusable when comparing Steam, Android, Switch, ordinary desktop Linux, and later deployment targets.
