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
| `atmega` | AVR instruction-set variants applicable to the pinned ATmega family/device |
| `attiny` | AVR instruction-set variants applicable to the pinned ATtiny family/device; reduced-core and AVRxt differences must remain explicit |
| `ch552` | WCH CH552 enhanced 8051-compatible CPU; WCH-specific differences must be separated from base MCS-51 |
| `esp` | Must pin the ESP chip: classic ESP32 is Xtensa LX6; later ESP32 family members use different Xtensa and RISC-V cores |
| `game-boy` | Sharp SM83 / LR35902-compatible Game Boy CPU instruction set |
| `msp430` | MSP430/MSP430X as applicable to the pinned device |
| `rp2040` | Armv6-M Thumb on Cortex-M0+ **and** the RP2040 PIO instruction set |
| `rp4080` | Unresolved target name: no current Raspberry Pi MCU named RP4080; do not invent an ISA |
| `steam` | Deployment product, not an ISA; pin concrete host CPU target(s), initially x86-64 if Steam Deck/PC-class hardware is intended |
| `switch` | Nintendo Switch CPU architecture boundary must be pinned separately from platform/GPU/runtime work |
| `tricore-aurix` | Pin the AURIX generation and corresponding TriCore ISA level rather than treating AURIX as one invariant ISA |
| `wasm` | WebAssembly Core Specification 3.0 |
| `webgpu` | WGSL language + WebGPU API/command/resource surface, not a fictional WebGPU machine ISA |

If a branch name is broader than a single ISA, completeness requires either pinning a concrete member or explicitly maintaining multiple inventories. Ambiguity is a blocker to declaring the inventory complete, not a reason to guess.
