# MSP430 / MSP430X instruction inventory

Status: architecture inventory, independent of Idriç implementation status.

Primary references: Texas Instruments MSP430 family user's guides, especially SLAU144K for the original MSP430 CPU and SLAU391F/SLAU208 for MSP430X CPUX. The branch is named for the architecture family rather than one device, so it records the union and distinguishes base MSP430 from MSP430X.

TI's original MSP430 core has 27 independently encoded instructions. The constant generator lets the assembler expose 24 additional emulated instructions, for the familiar 51-mnemonic programming surface. MSP430X is backward compatible and adds 20-bit address-word operations, extension-word forms, multi-bit shifts/rotates and multi-register stack operations.

## Original MSP430: real machine instructions

### Double-operand Format I

These are real opcodes; `.B` selects byte operation and the default/`.W` selects word operation where defined.

1. `MOV(.B) src,dst`
2. `ADD(.B) src,dst`
3. `ADDC(.B) src,dst`
4. `SUBC(.B) src,dst`
5. `SUB(.B) src,dst`
6. `CMP(.B) src,dst`
7. `DADD(.B) src,dst`
8. `BIT(.B) src,dst`
9. `BIC(.B) src,dst`
10. `BIS(.B) src,dst`
11. `XOR(.B) src,dst`
12. `AND(.B) src,dst`

### Single-operand Format II / special

13. `RRC(.B) dst`
14. `SWPB dst`
15. `RRA(.B) dst`
16. `SXT dst`
17. `PUSH(.B) src`
18. `CALL dst`
19. `RETI`

### Jump Format III

20. `JNE` / `JNZ label`
21. `JEQ` / `JZ label`
22. `JNC` / `JLO label`
23. `JC` / `JHS label`
24. `JN label`
25. `JGE label`
26. `JL label`
27. `JMP label`

The paired jump names are assembler aliases for the same encodings.

## Original MSP430: 24 TI-defined emulated instructions

These are part of the documented assembly-language instruction set but have no independent opcode; the assembler emits base instructions using the constant generator or ordinary addressing.

1. `ADC(.B) dst`
2. `BR dst`
3. `CLR(.B) dst`
4. `CLRC`
5. `CLRN`
6. `CLRZ`
7. `DADC(.B) dst`
8. `DEC(.B) dst`
9. `DECD(.B) dst`
10. `DINT`
11. `EINT`
12. `INC(.B) dst`
13. `INCD(.B) dst`
14. `INV(.B) dst`
15. `NOP`
16. `POP(.B) dst`
17. `RET`
18. `RLA(.B) dst`
19. `RLC(.B) dst`
20. `SBC(.B) dst`
21. `SETC`
22. `SETN`
23. `SETZ`
24. `TST(.B) dst`

Together with the 27 real encodings above this is TI's 51-instruction original MSP430 programming surface.

## MSP430X CPUX: extension-word versions of Format I operations

The MSP430X extension word extends the normal operations to the 20-bit address space and adds `.A` address-word width. The assembler-visible extended mnemonics are:

1. `MOVX(.B,.W,.A) src,dst`
2. `ADDX(.B,.W,.A) src,dst`
3. `ADDCX(.B,.W,.A) src,dst`
4. `SUBCX(.B,.W,.A) src,dst`
5. `SUBX(.B,.W,.A) src,dst`
6. `CMPX(.B,.W,.A) src,dst`
7. `DADDX(.B,.W,.A) src,dst`
8. `BITX(.B,.W,.A) src,dst`
9. `BICX(.B,.W,.A) src,dst`
10. `BISX(.B,.W,.A) src,dst`
11. `XORX(.B,.W,.A) src,dst`
12. `ANDX(.B,.W,.A) src,dst`

## MSP430X CPUX: extended single-operand operations

13. `RRCX(.B,.W,.A) dst`
14. `SWPBX(.W,.A) dst`
15. `RRAX(.B,.W,.A) dst`
16. `SXTX(.W,.A) dst`
17. `PUSHX(.B,.W,.A) src`
18. `CALLA dst` — multiple register/indexed/indirect/absolute/immediate 20-bit forms

`RETI` remains the architectural interrupt return encoding.

## MSP430X CPUX: multi-bit register operations

These encode a repeat count directly and operate on a register destination.

19. `RRCM.W #n,Rdst`
20. `RRCM.A #n,Rdst`
21. `RRAM.W #n,Rdst`
22. `RRAM.A #n,Rdst`
23. `RLAM.W #n,Rdst`
24. `RLAM.A #n,Rdst`
25. `RRUM.W #n,Rdst`
26. `RRUM.A #n,Rdst`

## MSP430X CPUX: multi-register stack operations

27. `PUSHM.W #n,Rdst`
28. `PUSHM.A #n,Rdst`
29. `POPM.W #n,Rdst`
30. `POPM.A #n,Rdst`

## MSP430X CPUX: compact 20-bit address instructions

These have restricted addressing modes and do not need the normal extension-word form.

31. `MOVA` — all documented forms: `@Rsrc,Rdst`, `@Rsrc+,Rdst`, `&abs20,Rdst`, `z16(Rsrc),Rdst`, `Rsrc,&abs20`, `Rsrc,z16(Rdst)`, `#imm20,Rdst`, `Rsrc,Rdst`
32. `CMPA #imm20,Rdst` / `CMPA Rsrc,Rdst`
33. `ADDA #imm20,Rdst` / `ADDA Rsrc,Rdst`
34. `SUBA #imm20,Rdst` / `SUBA Rsrc,Rdst`

`CALLA` belongs to the same 20-bit control-flow architecture and has its own multiple forms.

## MSP430X documented extended emulated instructions

These are assembler-visible MSP430X instructions with no independent opcode beyond the real X/address operations above:

1. `ADCX(.B,.W,.A) dst`
2. `BRA dst`
3. `RETA`
4. `CLRA Rdst`
5. `CLRX(.B,.W,.A) dst`
6. `DADCX(.B,.W,.A) dst`
7. `DECX(.B,.W,.A) dst`
8. `DECDA Rdst`
9. `DECDX(.B,.W,.A) dst`
10. `INCX(.B,.W,.A) dst`
11. `INCDA Rdst`
12. `INCDX(.B,.W,.A) dst`
13. `INVX(.B,.W,.A) dst`
14. `RLAX(.B,.W,.A) dst`
15. `RLCX(.B,.W,.A) dst`
16. `SBCX(.B,.W,.A) dst`
17. `TSTA Rdst`
18. `TSTX(.B,.W,.A) dst`
19. `POPX(.B,.W,.A) dst`

## Encoding families and addressing modes

A complete machine-readable encoding table must preserve the architecture's orthogonal fields rather than flattening every register/addressing combination into a fake mnemonic. Original MSP430 uses:

- 12 double-operand Format-I opcode families with source register/address mode, destination register/address mode, and byte/word bit;
- seven conditional/unconditional jump encodings with a signed 10-bit word displacement, with alias spellings above;
- Format-II single-operand encodings;
- constant-generator encodings through R2/R3.

MSP430X additionally uses:

- extension words carrying upper address bits, `.A` width and repeat information;
- compact 20-bit address instruction encodings (`MOVA`, `CMPA`, `ADDA`, `SUBA`);
- `CALLA` forms;
- multi-bit rotate/shift and multi-register push/pop encodings.

## Device boundary

The `msp430` branch is intentionally family-wide. A concrete device must be labeled `MSP430` or `MSP430X/CPUX` before backend support is claimed. The inventory above is the union; unsupported X instructions must not be silently attributed to a base-core device.

Idriç emission support belongs in a separate support table and must never filter the architecture inventory.
