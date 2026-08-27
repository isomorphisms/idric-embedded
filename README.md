# Idriç original Nintendo Switch platform target

This branch owns the public/reproducible platform path for the original Switch / Switch Lite / Switch OLED generation. Nintendo Switch is a platform, not one compiler ISA.

## Ownership

- generic AArch64 CPU codegen: `isomorphisms/idric-x86-aggressive-backend:a64-backend`;
- broad A64/SVE/SME architecture catalog: `isomorphisms/idric-big-iron:arch/aarch64-sve`;
- original-Switch Cortex-A57/Tegra-X1 feature mask, ABI/runtime, packaging, controller/display/audio/filesystem integration, and deployment: this branch;
- original-Switch Maxwell shader compiler: `isomorphisms/idris-shader-backend:target/switch-maxwell-sm53`.

`a64-backend` is currently only a designated scaffold; no executable A64 backend is claimed.

## Exact target boundary

The charged generation is Tegra X1/X1+ with Cortex-A57 AArch64 CPU execution and Maxwell GPU graphics. Do not silently add AArch32/T32. Switch 2/T239/Ampere is a separate future CPU profile, GPU target, and platform branch.

## Platform question

Given correct direct Idriç-generated A64 host code and a correct generated Maxwell shader, determine the additional public platform contracts required to make a reproducibly runnable Switch program:

- exact ABI/startup/object/executable boundary;
- libnx or another pinned public runtime path;
- deko3d/UAM host handoff without duplicating the shader compiler;
- deterministic frame, controller, audio, filesystem, timing, lifecycle, packaging, and launch evidence.

Keep the public/homebrew research path separate from Nintendo's official SDK, signing, certification, and retail publishing path.

Related issue: `isomorphisms/idric-embedded#5`.

