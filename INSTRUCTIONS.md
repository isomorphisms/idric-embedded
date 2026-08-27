# Steam target instruction inventory

Steam is a distribution/runtime target, not an instruction set.

## First concrete host target

Pin the first architecture target to **Steam Deck / SteamOS on AMD Zen 2**, i.e. AMD64/x86-64 user mode. Valve's current Steam Deck specifications identify the CPU as a 4-core/8-thread AMD Zen 2 CPU.

The complete CPU instruction inventory is therefore the same x86-64 architectural inventory maintained on:

`isomorphisms/idric-big-iron`, branch `arch/x86-64`

That inventory must preserve AMD/Intel extension membership rather than treating every x86 mnemonic as available on every CPU. For Steam Deck specifically, a later support matrix should select the feature set actually exposed by the Deck's Zen 2 APU and SteamOS ABI.

Do not create a separate fictional "Steam ISA" and do not duplicate x86 encoding facts with a divergent hand-maintained list.

## GPU boundary

Steam Deck's GPU is AMD RDNA 2. That does **not** mean ordinary Idriç host code targets an RDNA machine ISA. Graphics/compute code should use the separate shader/API target boundary selected for the game (for example SPIR-V/Vulkan or another explicit shader path) unless a deliberate native-GPU backend is created later.

If a native RDNA backend is ever created, it gets its own complete ISA inventory; it must not be smuggled into this CPU list.

## Other Steam machines

Steam runs on many PCs. Additional CPU architectures are separate deployment rows. A future Arm Steam target, for example, would reuse the appropriate AArch64 inventory rather than changing what "Steam" means.

## Completeness rule

For the current pinned Steam Deck target, architecture completeness means:

1. complete AMD64/x86-64 architecture data from `arch/x86-64`;
2. a Steam-Deck-specific CPU-feature availability mask;
3. Linux/SteamOS ABI and object-format notes kept separate from the ISA;
4. graphics/shader target kept separate from CPU code;
5. Idriç-supported x86 instructions kept as a separate subset.
