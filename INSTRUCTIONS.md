# `rp4080` target status

There is no Raspberry Pi microcontroller product named **RP4080** in the current documented RP2040/RP2350 family. This branch therefore must **not** contain an invented instruction list.

Status: target-name blocker. The architecture inventory is intentionally incomplete until the branch is renamed or the intended part is identified.

## If this branch was intended to mean RP2350 / Pico 2

RP2350 is substantially different from RP2040 and would require **three complete programmable-ISA inventories**, not one:

1. **Arm Cortex-M33**, implementing Armv8-M Main, configured on RP2350 with Security, DSP and FPU extensions;
2. **Hazard3 RISC-V**, selectable instead of Cortex-M33, with the silicon profile documented by Raspberry Pi;
3. **second-generation PIO**, separately programmable from either CPU architecture.

Raspberry Pi's RP2350 datasheet gives the Hazard3 standard RISC-V extension set as:

- RV32I
- M
- A
- C / Zca
- Zba
- Zbb
- Zbs
- Zbkb
- Zcb
- Zcmp
- Zicsr

and identifies custom Hazard3 extensions including `Xh3power`, `Xh3bextm`, `Xh3irq`, and `Xh3pmpm`. The datasheet contains an instruction-set reference for the implemented Hazard3 profile.

That is **not** interchangeable with the RP2040 Cortex-M0+ / Armv6-M + PIO-v0 inventory on the `rp2040` branch.

## Completion rule

Do not mark this branch complete until one of these happens:

- rename it to the intended real device and inventory every programmable ISA on that device; or
- document another real target that `rp4080` was intended to denote.

An unresolved branch name is preferable to a fabricated architecture.
