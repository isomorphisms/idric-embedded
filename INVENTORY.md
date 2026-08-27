# Architecture and language inventory invariant

Every target branch in this repository must preserve **complete target knowledge separately from the small Idriç subset that is implemented first**.

A branch is not considered inventoried merely because it links a manual or lists instruction families.

## CPU / virtual-machine ISA branches

For CPU and virtual-machine instruction sets, the branch must carry an exhaustive reproducible inventory containing:

- the exact ISA/core/specification revision;
- every architectural instruction mnemonic in the pinned scope;
- distinct encodings and operand/addressing forms where architecturally meaningful;
- flags/status effects and extension/version membership;
- aliases/pseudoinstructions separated from real encodings;
- privileged/system instructions retained even when Idriç does not emit them;
- source provenance and a reproducible generation path for large inventories;
- a separate table for the subset Idriç currently emits.

Board/product branches must identify **all programmable instruction sets actually in scope** (for example a CPU ISA plus a programmable-I/O ISA) rather than pretending the product name is an ISA.

## Shader/API branches

For targets such as WGSL/WebGPU that are not machine ISAs, use the analogous exhaustive surface:

- complete grammar/executable statement and expression surface;
- all types, address spaces, attributes and stage interfaces;
- all operators and built-in functions/values;
- all resource, command and synchronization operations in the pinned API scope;
- feature/extension membership;
- a separate table for what Idriç currently generates/uses.

Do not call portable shader-language operations native GPU opcodes.

## Current branches

| Branch | Target boundary |
| --- | --- |
| `atmega` | Complete 8-bit AVR instruction-name union, with AVR/AVRe/AVRxm/AVRxt/AVRrc and concrete-device availability kept explicit |
| `attiny` | Complete 8-bit AVR union, explicitly retaining reduced-core and AVRxt differences rather than assuming one ATtiny core |
| `ch552` | Complete MCS-51-compatible form surface plus the documented CH55x `0xA5` DPTR1 XRAM operation |
| `esp` | Separate Xtensa LX6/LX7 and RISC-V architecture inventories with per-chip configuration/extension filtering; no fictional single ESP ISA |
| `game-boy` | Complete Sharp SM83 / LR35902-compatible opcode space, including invalid base opcodes and all CB-prefixed operations |
| `msp430` | Complete MSP430/MSP430X real and documented emulated instruction surfaces, with core generation retained |
| `rp2040` | Complete Armv6-M Thumb Cortex-M0+ surface **and** the separate RP2040 PIO-v0 ISA |
| `rp4080` | Unresolved target name: no current Raspberry Pi MCU named RP4080; branch records the blocker instead of inventing an ISA |
| `steam` | First concrete deployment profile pinned to Steam Deck / SteamOS AMD64; complete x86-64 catalog is shared from `idric-big-iron` and filtered by Deck features |
| `switch` | Original Switch family pinned to Tegra X1 / Armv8-A A64 Cortex-A57/A53 profile; GPU/shader work remains a separate architecture boundary |
| `tricore-aurix` | Separate complete AURIX TC3xx / TriCore TC1.6.2P and TC4xx / TriCore TC1.8 inventories |
| `wasm` | Complete WebAssembly Core Specification 3.0 instruction table generated from the specification's own canonical instruction index source |
| `webgpu` | Complete pinned WGSL grammar/language and WebGPU API/command/resource surface; no fictional WebGPU machine ISA |

If a branch name is broader than a single ISA, completeness requires either pinning a concrete member or explicitly maintaining multiple inventories. Ambiguity is a blocker to declaring the inventory complete, not a reason to guess.
