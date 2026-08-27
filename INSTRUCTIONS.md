# Nintendo Switch target instruction inventory

Nintendo Switch is a platform, not an ISA. This branch now pins the first compiler architecture boundary to the **original Nintendo Switch family (Switch / Switch Lite / Switch OLED), not Nintendo Switch 2**.

Nintendo publicly describes the original family as using a custom NVIDIA Tegra processor. NVIDIA's Tegra X1 architecture documentation identifies its CPU complex as Arm Cortex-A57 plus Cortex-A53 cores implementing the 64-bit Armv8-A architecture.

## CPU instruction set

For generated 64-bit host code, the relevant ISA is **AArch64 / A64 for Armv8-A**, with the floating-point and Advanced SIMD facilities implemented by the Cortex-A57 target profile.

The exhaustive A64 instruction/encoding source is shared with:

`isomorphisms/idric-big-iron`, branch `arch/aarch64-sve`

but the Switch support mask is deliberately much narrower than that branch's full modern SVE/SVE2/SME architecture inventory:

- include the Armv8.0-A A64 base applicable to Cortex-A57;
- include the Cortex-A57 FP/Advanced SIMD profile;
- include only optional architectural extensions actually exposed by the target/toolchain;
- exclude SVE, SVE2, SME and later Armv8.x/Armv9 facilities that do not exist on Tegra X1.

The shared A64 catalog supplies instruction identity/encoding facts; the Switch feature mask supplies availability.

## AArch32/T32

Cortex-A57 also implements AArch32 execution state. Do not silently include A32/T32 in the first Idriç Switch backend merely because the hardware can execute it. If 32-bit Switch code becomes an actual target, add a complete A32/T32 inventory as a separate architecture profile.

## GPU boundary

The original Tegra X1 integrates an NVIDIA Maxwell-generation GPU. That native GPU ISA is not the CPU ISA and is not the first compiler boundary here. Game shaders should target the explicit graphics/shader representation used by the platform tooling. A direct Maxwell backend, if ever attempted, must get its own separately sourced complete native-GPU instruction inventory.

## Switch 2 is a different target

Nintendo's current Switch 2 specifications describe only a custom NVIDIA processor publicly; third-party technical analysis identifies a substantially newer Arm/NVIDIA design. Do not mix Switch 2 instruction availability into this original-Switch branch. If targeted, create a distinct profile/branch and pin it from public authoritative material available at that time.

## Completeness rule

For the original Switch CPU target:

1. use the complete shared A64 catalog;
2. apply the exact Cortex-A57/Tegra-X1 feature/version mask;
3. keep ABI/platform/runtime material separate;
4. keep GPU/shader compilation separate;
5. keep Idriç-supported instructions as a separate subset.
