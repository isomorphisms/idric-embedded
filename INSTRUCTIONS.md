# Game Boy SM83 complete opcode inventory

Status: exhaustive architecture inventory, independent of Idriç implementation status.

Primary reference: gbdev Pan Docs / Game Boy CPU (SM83) instruction tables. The Game Boy CPU has a 256-byte base opcode space. Opcode `CB` introduces a second 256-entry table. Eleven base opcodes are invalid/hard-lock opcodes.

Notation:

- `r8` ordering is `B C D E H L [HL] A`.
- `r16` ordering where used is `BC DE HL SP`.
- `r16stk` ordering is `BC DE HL AF`.
- `cond` ordering is `NZ Z NC C`.
- `n8`, `n16` are immediate unsigned values; `e8` is signed relative displacement; `a8`, `a16` are addresses.
- `HL+` and `HL-` mean use `[HL]` then increment/decrement HL.

## Base opcode table: 00–3F

| Opcode | Instruction |
| --- | --- |
| 00 | `NOP` |
| 01 | `LD BC,n16` |
| 02 | `LD [BC],A` |
| 03 | `INC BC` |
| 04 | `INC B` |
| 05 | `DEC B` |
| 06 | `LD B,n8` |
| 07 | `RLCA` |
| 08 | `LD [a16],SP` |
| 09 | `ADD HL,BC` |
| 0A | `LD A,[BC]` |
| 0B | `DEC BC` |
| 0C | `INC C` |
| 0D | `DEC C` |
| 0E | `LD C,n8` |
| 0F | `RRCA` |
| 10 | `STOP n8` |
| 11 | `LD DE,n16` |
| 12 | `LD [DE],A` |
| 13 | `INC DE` |
| 14 | `INC D` |
| 15 | `DEC D` |
| 16 | `LD D,n8` |
| 17 | `RLA` |
| 18 | `JR e8` |
| 19 | `ADD HL,DE` |
| 1A | `LD A,[DE]` |
| 1B | `DEC DE` |
| 1C | `INC E` |
| 1D | `DEC E` |
| 1E | `LD E,n8` |
| 1F | `RRA` |
| 20 | `JR NZ,e8` |
| 21 | `LD HL,n16` |
| 22 | `LD [HL+],A` |
| 23 | `INC HL` |
| 24 | `INC H` |
| 25 | `DEC H` |
| 26 | `LD H,n8` |
| 27 | `DAA` |
| 28 | `JR Z,e8` |
| 29 | `ADD HL,HL` |
| 2A | `LD A,[HL+]` |
| 2B | `DEC HL` |
| 2C | `INC L` |
| 2D | `DEC L` |
| 2E | `LD L,n8` |
| 2F | `CPL` |
| 30 | `JR NC,e8` |
| 31 | `LD SP,n16` |
| 32 | `LD [HL-],A` |
| 33 | `INC SP` |
| 34 | `INC [HL]` |
| 35 | `DEC [HL]` |
| 36 | `LD [HL],n8` |
| 37 | `SCF` |
| 38 | `JR C,e8` |
| 39 | `ADD HL,SP` |
| 3A | `LD A,[HL-]` |
| 3B | `DEC SP` |
| 3C | `INC A` |
| 3D | `DEC A` |
| 3E | `LD A,n8` |
| 3F | `CCF` |

## Base opcode table: 40–7F

This range is the complete 8×8 `LD destination,source` matrix over `r8 = B,C,D,E,H,L,[HL],A`, except opcode `76` is `HALT` rather than `LD [HL],[HL]`.

|       | B | C | D | E | H | L | [HL] | A |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B | 40 `LD B,B` | 41 `LD B,C` | 42 `LD B,D` | 43 `LD B,E` | 44 `LD B,H` | 45 `LD B,L` | 46 `LD B,[HL]` | 47 `LD B,A` |
| C | 48 `LD C,B` | 49 `LD C,C` | 4A `LD C,D` | 4B `LD C,E` | 4C `LD C,H` | 4D `LD C,L` | 4E `LD C,[HL]` | 4F `LD C,A` |
| D | 50 `LD D,B` | 51 `LD D,C` | 52 `LD D,D` | 53 `LD D,E` | 54 `LD D,H` | 55 `LD D,L` | 56 `LD D,[HL]` | 57 `LD D,A` |
| E | 58 `LD E,B` | 59 `LD E,C` | 5A `LD E,D` | 5B `LD E,E` | 5C `LD E,H` | 5D `LD E,L` | 5E `LD E,[HL]` | 5F `LD E,A` |
| H | 60 `LD H,B` | 61 `LD H,C` | 62 `LD H,D` | 63 `LD H,E` | 64 `LD H,H` | 65 `LD H,L` | 66 `LD H,[HL]` | 67 `LD H,A` |
| L | 68 `LD L,B` | 69 `LD L,C` | 6A `LD L,D` | 6B `LD L,E` | 6C `LD L,H` | 6D `LD L,L` | 6E `LD L,[HL]` | 6F `LD L,A` |
| [HL] | 70 `LD [HL],B` | 71 `LD [HL],C` | 72 `LD [HL],D` | 73 `LD [HL],E` | 74 `LD [HL],H` | 75 `LD [HL],L` | 76 `HALT` | 77 `LD [HL],A` |
| A | 78 `LD A,B` | 79 `LD A,C` | 7A `LD A,D` | 7B `LD A,E` | 7C `LD A,H` | 7D `LD A,L` | 7E `LD A,[HL]` | 7F `LD A,A` |

## Base opcode table: 80–BF

Each row is an 8-entry operation over `r8 = B,C,D,E,H,L,[HL],A`.

| Opcodes | Operation |
| --- | --- |
| 80–87 | `ADD A,r8` |
| 88–8F | `ADC A,r8` |
| 90–97 | `SUB A,r8` |
| 98–9F | `SBC A,r8` |
| A0–A7 | `AND A,r8` |
| A8–AF | `XOR A,r8` |
| B0–B7 | `OR A,r8` |
| B8–BF | `CP A,r8` |

Expanded opcode identity is the low three bits selecting `B,C,D,E,H,L,[HL],A` in that order.

## Base opcode table: C0–FF

| Opcode | Instruction |
| --- | --- |
| C0 | `RET NZ` |
| C1 | `POP BC` |
| C2 | `JP NZ,a16` |
| C3 | `JP a16` |
| C4 | `CALL NZ,a16` |
| C5 | `PUSH BC` |
| C6 | `ADD A,n8` |
| C7 | `RST 00H` |
| C8 | `RET Z` |
| C9 | `RET` |
| CA | `JP Z,a16` |
| CB | `PREFIX CB` |
| CC | `CALL Z,a16` |
| CD | `CALL a16` |
| CE | `ADC A,n8` |
| CF | `RST 08H` |
| D0 | `RET NC` |
| D1 | `POP DE` |
| D2 | `JP NC,a16` |
| D3 | **invalid / hard lock** |
| D4 | `CALL NC,a16` |
| D5 | `PUSH DE` |
| D6 | `SUB A,n8` |
| D7 | `RST 10H` |
| D8 | `RET C` |
| D9 | `RETI` |
| DA | `JP C,a16` |
| DB | **invalid / hard lock** |
| DC | `CALL C,a16` |
| DD | **invalid / hard lock** |
| DE | `SBC A,n8` |
| DF | `RST 18H` |
| E0 | `LDH [a8],A` |
| E1 | `POP HL` |
| E2 | `LDH [C],A` |
| E3 | **invalid / hard lock** |
| E4 | **invalid / hard lock** |
| E5 | `PUSH HL` |
| E6 | `AND A,n8` |
| E7 | `RST 20H` |
| E8 | `ADD SP,e8` |
| E9 | `JP HL` |
| EA | `LD [a16],A` |
| EB | **invalid / hard lock** |
| EC | **invalid / hard lock** |
| ED | **invalid / hard lock** |
| EE | `XOR A,n8` |
| EF | `RST 28H` |
| F0 | `LDH A,[a8]` |
| F1 | `POP AF` |
| F2 | `LDH A,[C]` |
| F3 | `DI` |
| F4 | **invalid / hard lock** |
| F5 | `PUSH AF` |
| F6 | `OR A,n8` |
| F7 | `RST 30H` |
| F8 | `LD HL,SP+e8` |
| F9 | `LD SP,HL` |
| FA | `LD A,[a16]` |
| FB | `EI` |
| FC | **invalid / hard lock** |
| FD | **invalid / hard lock** |
| FE | `CP A,n8` |
| FF | `RST 38H` |

The eleven invalid base opcodes are exactly:

`D3 DB DD E3 E4 EB EC ED F4 FC FD`

## CB-prefixed opcode table: CB00–CB3F

Each operation expands over `r8 = B,C,D,E,H,L,[HL],A`.

| Sub-opcodes | Operation |
| --- | --- |
| 00–07 | `RLC r8` |
| 08–0F | `RRC r8` |
| 10–17 | `RL r8` |
| 18–1F | `RR r8` |
| 20–27 | `SLA r8` |
| 28–2F | `SRA r8` |
| 30–37 | `SWAP r8` |
| 38–3F | `SRL r8` |

For every row the low three bits select `B,C,D,E,H,L,[HL],A`, so this table identifies all 64 encodings exactly.

## CB-prefixed opcode table: CB40–CB7F — BIT

`CB40`–`CB7F` is the complete Cartesian product:

`BIT bit,r8` where `bit = 0..7` and `r8 = B,C,D,E,H,L,[HL],A`.

Encoding identity:

- `CB40`–`CB47`: `BIT 0,r8`
- `CB48`–`CB4F`: `BIT 1,r8`
- `CB50`–`CB57`: `BIT 2,r8`
- `CB58`–`CB5F`: `BIT 3,r8`
- `CB60`–`CB67`: `BIT 4,r8`
- `CB68`–`CB6F`: `BIT 5,r8`
- `CB70`–`CB77`: `BIT 6,r8`
- `CB78`–`CB7F`: `BIT 7,r8`

## CB-prefixed opcode table: CB80–CBBF — RES

`CB80`–`CBBF` is the complete Cartesian product:

`RES bit,r8` where `bit = 0..7` and `r8 = B,C,D,E,H,L,[HL],A`.

- `CB80`–`CB87`: `RES 0,r8`
- `CB88`–`CB8F`: `RES 1,r8`
- `CB90`–`CB97`: `RES 2,r8`
- `CB98`–`CB9F`: `RES 3,r8`
- `CBA0`–`CBA7`: `RES 4,r8`
- `CBA8`–`CBAF`: `RES 5,r8`
- `CBB0`–`CBB7`: `RES 6,r8`
- `CBB8`–`CBBF`: `RES 7,r8`

## CB-prefixed opcode table: CBC0–CBFF — SET

`CBC0`–`CBFF` is the complete Cartesian product:

`SET bit,r8` where `bit = 0..7` and `r8 = B,C,D,E,H,L,[HL],A`.

- `CBC0`–`CBC7`: `SET 0,r8`
- `CBC8`–`CBCF`: `SET 1,r8`
- `CBD0`–`CBD7`: `SET 2,r8`
- `CBD8`–`CBDF`: `SET 3,r8`
- `CBE0`–`CBE7`: `SET 4,r8`
- `CBE8`–`CBEF`: `SET 5,r8`
- `CBF0`–`CBF7`: `SET 6,r8`
- `CBF8`–`CBFF`: `SET 7,r8`

## Aliases

Pan Docs and assemblers may use alternate spellings such as `LDH` versus `LD [FF00+a8],...`, `HLI`/`HLD` for HL auto-increment/decrement forms, or omit the explicit `A` operand on some arithmetic mnemonics. Those are syntax aliases, not extra machine opcodes.

## Completeness statement

This file covers every byte in the 256-entry base opcode space and every byte in the 256-entry CB-prefixed space, including invalid base opcodes. Idriç emission support belongs in a separate support table and must never filter this architecture inventory.
