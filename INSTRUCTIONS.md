# RP2040 complete programmable instruction inventory

Status: architecture inventory, independent of Idriç implementation status.

RP2040 contains **two distinct programmable instruction sets** that matter to this repository:

1. two Arm Cortex-M0+ CPU cores implementing Armv6-M Thumb;
2. two PIO blocks whose eight state machines execute the RP2040 PIO version-0 instruction set.

These must not be collapsed into one list.

# 1. Cortex-M0+ / Armv6-M Thumb

Primary device reference: RP2040 Datasheet, §2.4.3.3. Raspberry Pi states that the core implements Armv6-M Thumb: all applicable 16-bit Thumb instructions, excluding the Armv7-M-only `CBZ`, `CBNZ`, and `IT`, plus the 32-bit Thumb instructions `BL`, `DMB`, `DSB`, `ISB`, `MRS`, and `MSR`.

The following is the complete assembler-visible operation/form inventory from the RP2040 Cortex-M0+ instruction summary, with architectural aliases noted rather than counted as new opcodes.

## Move and address generation

- `MOVS Rd,#imm8`
- `MOVS Rd,Rm` — low-register form
- `MOV Rd,Rm` — high/any-register form
- `MOV PC,Rm`
- `ADR Rd,label`

## Add/subtract/multiply

- `ADDS Rd,Rn,#imm3`
- `ADDS Rd,Rn,Rm`
- `ADD Rd,Rd,Rm` — high-register form
- `ADD PC,PC,Rm`
- `ADDS Rd,Rd,#imm8`
- `ADCS Rd,Rd,Rm`
- `ADD SP,SP,#imm`
- `ADD Rd,SP,#imm`
- `SUBS Rd,Rn,Rm`
- `SUBS Rd,Rn,#imm3`
- `SUBS Rd,Rd,#imm8`
- `SBCS Rd,Rd,Rm`
- `SUB SP,SP,#imm`
- `RSBS Rd,Rn,#0`
- `MULS Rd,Rm,Rd`

## Compare/test/logical

- `CMP Rn,Rm`
- `CMP Rn,#imm8`
- `CMN Rn,Rm`
- `ANDS Rd,Rd,Rm`
- `EORS Rd,Rd,Rm`
- `ORRS Rd,Rd,Rm`
- `BICS Rd,Rd,Rm`
- `MVNS Rd,Rm`
- `TST Rn,Rm`

## Shifts and rotate

- `LSLS Rd,Rm,#shift`
- `LSLS Rd,Rd,Rs`
- `LSRS Rd,Rm,#shift`
- `LSRS Rd,Rd,Rs`
- `ASRS Rd,Rm,#shift`
- `ASRS Rd,Rd,Rs`
- `RORS Rd,Rd,Rs`

## Loads

- `LDR Rd,[Rn,#imm]` — word immediate offset
- `LDRH Rd,[Rn,#imm]` — halfword immediate offset
- `LDRB Rd,[Rn,#imm]` — byte immediate offset
- `LDR Rd,[Rn,Rm]` — word register offset
- `LDRH Rd,[Rn,Rm]`
- `LDRSH Rd,[Rn,Rm]`
- `LDRB Rd,[Rn,Rm]`
- `LDRSB Rd,[Rn,Rm]`
- `LDR Rd,label` — PC-relative literal load
- `LDR Rd,[SP,#imm]`
- `LDM Rn!,{low-register-list}` — base excluded
- `LDM Rn,{low-register-list}` — base included; writeback behavior differs

`LDMIA` is an accepted architectural/assembler spelling for the Thumb load-multiple form, not another independent instruction family.

## Stores

- `STR Rd,[Rn,#imm]`
- `STRH Rd,[Rn,#imm]`
- `STRB Rd,[Rn,#imm]`
- `STR Rd,[Rn,Rm]`
- `STRH Rd,[Rn,Rm]`
- `STRB Rd,[Rn,Rm]`
- `STR Rd,[SP,#imm]`
- `STM Rn!,{low-register-list}`

`STMIA` is the corresponding alias/spelling for the increment-after multiple-store form.

## Stack

- `PUSH {low-register-list}`
- `PUSH {low-register-list,LR}`
- `POP {low-register-list}`
- `POP {low-register-list,PC}`

## Branch/control flow

- `B<cc> label` for each Armv6-M condition encoding allowed on the 16-bit conditional branch
- `B label`
- `BL label` — 32-bit Thumb
- `BX Rm`
- `BLX Rm`

The condition-name aliases (`CS`/`HS`, `CC`/`LO`) refer to the same encodings.

## Extend/reverse

- `SXTH Rd,Rm`
- `SXTB Rd,Rm`
- `UXTH Rd,Rm`
- `UXTB Rd,Rm`
- `REV Rd,Rm`
- `REV16 Rd,Rm`
- `REVSH Rd,Rm`

## Exceptions, privilege, special registers and breakpoint

- `SVC #imm8`
- `CPSID i`
- `CPSIE i`
- `MRS Rd,specreg` — 32-bit Thumb
- `MSR specreg,Rn` — 32-bit Thumb
- `BKPT #imm8`
- `UDF #imm` — architecturally permanently undefined encoding; retained in the architecture inventory even though it is not a normal generated computation instruction

## Hints

- `NOP`
- `YIELD`
- `WFE`
- `WFI`
- `SEV`

## Barriers

- `DMB` — 32-bit Thumb
- `DSB` — 32-bit Thumb
- `ISB` — 32-bit Thumb

## Explicit exclusions for RP2040's Armv6-M core

Do **not** attribute `CBZ`, `CBNZ`, or `IT` to RP2040. They are not in its Armv6-M Thumb profile. Likewise there is no Cortex-M4/M7 DSP or floating-point instruction extension on RP2040's M0+ cores.

# 2. RP2040 PIO version-0 ISA

PIO instructions are 16 bits. Bits 15:13 select one of eight major encodings; `PUSH` and `PULL` share major opcode `100`. Every real PIO instruction also contains the common five-bit delay/side-set field, partitioned by state-machine configuration.

## Major opcode map

| Bits 15:13 | Instruction |
| --- | --- |
| `000` | `JMP` |
| `001` | `WAIT` |
| `010` | `IN` |
| `011` | `OUT` |
| `100` | `PUSH` / `PULL` |
| `101` | `MOV` |
| `110` | `IRQ` |
| `111` | `SET` |

## `JMP`

Form: `jmp (condition) address`

All eight condition-field values:

- `000`: always
- `001`: `!X` — X is zero
- `010`: `X--` — branch if X was nonzero, then decrement X
- `011`: `!Y` — Y is zero
- `100`: `Y--` — branch if Y was nonzero, then decrement Y
- `101`: `X!=Y`
- `110`: `PIN`
- `111`: `!OSRE`

Address is the absolute five-bit PIO instruction-memory address after relocation.

## `WAIT`

Forms:

- `wait polarity gpio gpio_num`
- `wait polarity pin pin_num`
- `wait polarity irq irq_num`
- `wait polarity irq irq_num rel`

Polarity is `0` or `1`.

Source-field values:

- `00`: GPIO
- `01`: PIN
- `10`: IRQ
- `11`: reserved

For IRQ, the relative form adds the state-machine number modulo four to the low two IRQ-index bits.

## `IN`

Form: `in source,bit_count`, where bit count is 1..32 (`32` encoded as zero).

All source-field values:

- `000`: PINS
- `001`: X
- `010`: Y
- `011`: NULL
- `100`: reserved
- `101`: reserved
- `110`: ISR
- `111`: OSR

## `OUT`

Form: `out destination,bit_count`, where bit count is 1..32 (`32` encoded as zero).

All destination-field values:

- `000`: PINS
- `001`: X
- `010`: Y
- `011`: NULL
- `100`: PINDIRS
- `101`: PC
- `110`: ISR
- `111`: EXEC

## `PUSH`

Encoding parameters are `IfFull` and `Block`.

Assembler surface:

- `push`
- `push iffull`
- `push block` — `block` is default
- `push noblock`
- `push iffull block`
- `push iffull noblock`

The semantic bit combinations are the Cartesian product `IfFull ∈ {0,1}` × `Block ∈ {0,1}`.

## `PULL`

Encoding parameters are `IfEmpty` and `Block`.

Assembler surface:

- `pull`
- `pull ifempty`
- `pull block` — `block` is default
- `pull noblock`
- `pull ifempty block`
- `pull ifempty noblock`

Again the semantic bit combinations are the full `IfEmpty ∈ {0,1}` × `Block ∈ {0,1}` product.

## `MOV`

Form: `mov destination,(operation) source`.

Destination-field values:

- `000`: PINS
- `001`: X
- `010`: Y
- `011`: reserved
- `100`: EXEC
- `101`: PC
- `110`: ISR
- `111`: OSR

Operation-field values:

- `00`: identity
- `01`: bitwise invert (`!` or `~`)
- `10`: 32-bit bit reverse (`::`)
- `11`: reserved

Source-field values:

- `000`: PINS
- `001`: X
- `010`: Y
- `011`: NULL
- `100`: reserved
- `101`: STATUS
- `110`: ISR
- `111`: OSR

Legal MOV encodings are combinations of non-reserved destination, operation, and source values, subject to the architecture semantics above.

## `IRQ`

Assembler spellings:

- `irq n`
- `irq set n`
- `irq nowait n`
- `irq wait n`
- `irq clear n`

Each can use the relative IRQ-index mode where valid. `irq`, `irq set`, and `irq nowait` are aliases for the same set-without-wait behavior. The encoding independently records Clear, Wait, and the IRQ index/relative bit.

## `SET`

Form: `set destination,value`, value 0..31.

Destination-field values:

- `000`: PINS
- `001`: X
- `010`: Y
- `011`: reserved
- `100`: PINDIRS
- `101`: reserved
- `110`: reserved
- `111`: reserved

## PIO pseudoinstruction

`nop` is not a ninth hardware opcode. `pioasm` assembles it as `mov y,y`; it is useful as a carrier for delay or side-set.

## Common delay / side-set field

Every real PIO instruction carries five bits whose interpretation depends on `SIDESET_COUNT`:

- low bits encode 0..31 delay cycles when not consumed by side-set;
- high bits encode the configured side-set value;
- optional side-set configuration can consume an enable bit as defined by the assembler/state-machine setup.

This common field is part of every instruction encoding and therefore belongs in the exhaustive architecture record, even though it does not create separate mnemonics.

# Completeness rule

The CPU list above follows the RP2040 Cortex-M0+ Armv6-M implementation boundary. The PIO section covers every major opcode, every selector field value including reserved values, every assembler-visible real instruction family, and the sole documented `nop` pseudoinstruction.

Idriç CPU lowering and any future Idriç PIO generation are separate support matrices.
