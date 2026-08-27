# ESP architecture instruction inventory

Status: family-wide architecture inventory. Idriç support is tracked separately.

`esp` is not one ISA. Current ESP32-family targets represented by this branch span at least:

| Chip family | Main programmable CPU ISA |
| --- | --- |
| classic ESP32 | Xtensa LX6, Espressif configuration |
| ESP32-S2 | Xtensa LX7, Espressif configuration; separate ULP RISC-V/FSM coprocessor |
| ESP32-S3 | Xtensa LX7, Espressif configuration; separate ULP RISC-V/FSM coprocessor |
| ESP32-C3 | RV32IMC plus the architectural CSR/fence pieces used by the toolchain |
| ESP32-C6 | RV32IMAC plus `Zicsr`/`Zifencei`; separate LP RISC-V core |
| ESP32-H2 | RV32IMAC plus `Zicsr`/`Zifencei` |
| ESP32-P4 | RISC-V HP and LP cores; exact core-specific extension sets must be kept separate |

Do not merge these into a fictional "ESP instruction set".

## Xtensa source of truth

Pin the public Espressif Xtensa ISA source at:

- repository: `espressif/xtensa-isa-doc`
- commit: `00216044559526727d058feffc8fd09957d96b19`

That source explicitly exists for compiler/tool authors and contains the base ISA plus ISA extensions used by Espressif SoCs. `tools/extract-xtensa-instructions.py` on this branch extracts every assembler-visible instruction from every `Instructions*.tex` file and the code-density material.

A concrete Xtensa chip inventory is the extracted union **filtered by that chip's generated Xtensa configuration**, in particular `components/xtensa/<chip>/include/xtensa/config/core-isa.h` in the pinned ESP-IDF release. Those configuration macros determine optional operations such as MIN/MAX, SEXT, CLAMPS, multiply/divide, atomics, code density, windowed registers, FP and other configured features.

This is necessary because Xtensa is configurable: `LX6` or `LX7` alone is not enough to prove that one optional instruction exists on a particular ESP chip.

## RISC-V RV32I base instruction set

Every instruction below is a real architectural instruction, not a pseudoinstruction:

`LUI AUIPC JAL JALR BEQ BNE BLT BGE BLTU BGEU LB LH LW LBU LHU SB SH SW ADDI SLTI SLTIU XORI ORI ANDI SLLI SRLI SRAI ADD SUB SLL SLT SLTU XOR SRL SRA OR AND FENCE ECALL EBREAK`

## M extension

`MUL MULH MULHSU MULHU DIV DIVU REM REMU`

## A extension, RV32 word operations

`LR.W SC.W AMOSWAP.W AMOADD.W AMOXOR.W AMOAND.W AMOOR.W AMOMIN.W AMOMAX.W AMOMINU.W AMOMAXU.W`

The `aq` and `rl` bits are encoding/ordering modifiers on these instructions, not new mnemonics.

## C extension, RV32 compressed instructions

`C.ADDI4SPN C.LW C.SW C.NOP C.ADDI C.JAL C.LI C.ADDI16SP C.LUI C.SRLI C.SRAI C.ANDI C.SUB C.XOR C.OR C.AND C.J C.BEQZ C.BNEZ C.SLLI C.LWSP C.JR C.MV C.EBREAK C.JALR C.ADD C.SWSP`

`C.JAL` is the RV32 form; extension-version restrictions must remain explicit if the branch later pins a newer compressed-extension profile.

## Zicsr

`CSRRW CSRRS CSRRC CSRRWI CSRRSI CSRRCI`

## Zifencei

`FENCE.I`

## Privileged execution surface used by ESP RISC-V cores

Privileged instructions such as `MRET` and `WFI` belong in the per-chip machine-mode inventory when implemented. Privilege levels, PMP, interrupt-controller behavior and CSR existence are chip/core facts and must be taken from the corresponding Espressif technical reference rather than inferred from `RV32IMAC` alone.

## Assembler pseudoinstructions

Names such as `NOP`, `LI`, `MV`, `NOT`, `NEG`, `SEQZ`, `SNEZ`, `SLTZ`, `SGTZ`, `BEQZ`, `BNEZ`, `BLEZ`, `BGEZ`, `BLTZ`, `BGTZ`, `J`, `JR`, `RET`, `CALL`, `TAIL`, `LA`, and CSR convenience spellings are useful assembler syntax but must be recorded as aliases/pseudoinstructions, not counted as additional RISC-V machine encodings.

## Completeness rule

For a chosen ESP chip, the branch is complete only when all of the following are true:

1. the chip is named exactly;
2. its main-core ISA and every separately programmable low-power/core ISA are named;
3. the Xtensa extractor or RISC-V extension inventory covers every instruction in that ISA;
4. chip configuration/extension flags are applied;
5. custom Espressif instructions, if any, are added from the chip's authoritative toolchain/reference material;
6. Idriç-emitted instructions are a separate support matrix.

The family table above prevents a broad `esp` branch from silently pretending that LX6, LX7 and RV32IMAC are interchangeable.
