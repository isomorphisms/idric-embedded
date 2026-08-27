# CH552 enhanced E8051 instruction inventory

Status: architecture inventory, independent of Idriç implementation status.

The CH552 uses WCH's enhanced 1T E8051 core and is compatible with the MCS-51 instruction set. WCH also documents a CH55x-specific opcode `0xA5` for a fast XRAM-copy primitive using the second data pointer.

This file records the complete assembler-visible MCS-51 instruction/form surface plus that documented CH552 extension. Register families are expanded symbolically (`Rn` = R0..R7, `@Ri` = @R0/@R1); each expansion corresponds to its normal distinct opcode encoding.

## Complete MCS-51 instruction forms

### Calls and jumps

- `ACALL addr11`
- `AJMP addr11`
- `LCALL addr16`
- `LJMP addr16`
- `SJMP rel`
- `JMP @A+DPTR`
- `JB bit,rel`
- `JBC bit,rel`
- `JNB bit,rel`
- `JC rel`
- `JNC rel`
- `JZ rel`
- `JNZ rel`
- `DJNZ Rn,rel`
- `DJNZ direct,rel`
- `CJNE A,direct,rel`
- `CJNE A,#data,rel`
- `CJNE Rn,#data,rel`
- `CJNE @Ri,#data,rel`
- `RET`
- `RETI`

### Addition, subtraction, multiply/divide, decimal adjust

- `ADD A,Rn`
- `ADD A,direct`
- `ADD A,@Ri`
- `ADD A,#data`
- `ADDC A,Rn`
- `ADDC A,direct`
- `ADDC A,@Ri`
- `ADDC A,#data`
- `SUBB A,Rn`
- `SUBB A,direct`
- `SUBB A,@Ri`
- `SUBB A,#data`
- `INC A`
- `INC Rn`
- `INC direct`
- `INC @Ri`
- `INC DPTR`
- `DEC A`
- `DEC Rn`
- `DEC direct`
- `DEC @Ri`
- `MUL AB`
- `DIV AB`
- `DA A`

### Boolean/bit operations

- `CLR A`
- `CLR C`
- `CLR bit`
- `CPL A`
- `CPL C`
- `CPL bit`
- `SETB C`
- `SETB bit`
- `ANL C,bit`
- `ANL C,/bit`
- `ORL C,bit`
- `ORL C,/bit`
- `MOV C,bit`
- `MOV bit,C`

### Byte logical operations

- `ANL A,Rn`
- `ANL A,direct`
- `ANL A,@Ri`
- `ANL A,#data`
- `ANL direct,A`
- `ANL direct,#data`
- `ORL A,Rn`
- `ORL A,direct`
- `ORL A,@Ri`
- `ORL A,#data`
- `ORL direct,A`
- `ORL direct,#data`
- `XRL A,Rn`
- `XRL A,direct`
- `XRL A,@Ri`
- `XRL A,#data`
- `XRL direct,A`
- `XRL direct,#data`

### Rotates and nibble operations

- `RL A`
- `RLC A`
- `RR A`
- `RRC A`
- `SWAP A`

### Internal data movement

- `MOV A,Rn`
- `MOV A,direct`
- `MOV A,@Ri`
- `MOV A,#data`
- `MOV Rn,A`
- `MOV Rn,direct`
- `MOV Rn,#data`
- `MOV direct,A`
- `MOV direct,Rn`
- `MOV direct,direct`
- `MOV direct,@Ri`
- `MOV direct,#data`
- `MOV @Ri,A`
- `MOV @Ri,direct`
- `MOV @Ri,#data`
- `MOV DPTR,#data16`

### Program-memory reads

- `MOVC A,@A+DPTR`
- `MOVC A,@A+PC`

### External/XRAM movement

- `MOVX A,@Ri`
- `MOVX A,@DPTR`
- `MOVX @Ri,A`
- `MOVX @DPTR,A`

### Exchange

- `XCH A,Rn`
- `XCH A,direct`
- `XCH A,@Ri`
- `XCHD A,@Ri`

### Stack and no-op

- `PUSH direct`
- `POP direct`
- `NOP`

## CH552/WCH extension

### `0xA5` — `MOVX @DPTR1,A` + increment DPTR1

WCH's CH552/CH554 headers document opcode byte `0xA5` as a new one-cycle instruction:

1. write `A` to on-chip XRAM at the address in `DPTR1`;
2. increment `DPTR1`.

DPTR0/DPTR1 selection/configuration is controlled through the CH55x auxiliary bus/SFR mechanism; the second pointer is architectural device state, not another generic MCS-51 opcode family.

## Canonical mnemonic set

The base MCS-51 mnemonic set represented above is:

`ACALL ADD ADDC AJMP ANL CJNE CLR CPL DA DEC DIV DJNZ INC JB JBC JC JMP JNB JNC JNZ JZ LCALL LJMP MOV MOVC MOVX MUL NOP ORL POP PUSH RET RETI RL RLC RR RRC SETB SJMP SUBB SWAP XCH XCHD XRL`

CH552 adds the documented `0xA5` `MOVX @DPTR1,A`/auto-increment form.

## Completeness boundary

Peripheral SFR operations are ordinary MCS-51 data/bit instructions applied to CH552-specific addresses; they are not separate CPU opcodes. DMA/USB/SPI/timer behavior therefore belongs in a device-register inventory, not this CPU instruction list.

Idriç support is a separate table. An instruction is not removed from this file merely because the compiler never emits it.
