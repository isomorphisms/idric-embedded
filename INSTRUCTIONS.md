# AVR instruction inventory for ATtiny targets

Status: architecture inventory, independent of Idriç implementation status.

Primary source: Microchip **AVR Instruction Set Manual**, DS40002198C (11/2024). The manual explicitly distinguishes AVR, AVRe, AVRxm, AVRxt and reduced-core AVRrc and gives per-device availability in its appendix.

ATtiny spans materially different AVR cores: older reduced-core devices and newer tinyAVR devices cannot be represented honestly by one unannotated subset. This branch therefore records the **complete 8-bit AVR instruction-name union**. Once a concrete ATtiny device is selected, mark its exact core and availability against this union.

## Complete instruction-description inventory

1. `ADC` — Add with Carry
2. `ADD` — Add without Carry
3. `ADIW` — Add Immediate to Word
4. `AND` — Logical AND
5. `ANDI` — Logical AND with Immediate
6. `ASR` — Arithmetic Shift Right
7. `BCLR` — Bit Clear in SREG
8. `BLD` — Bit Load from T to register bit
9. `BRBC` — Branch if SREG bit cleared
10. `BRBS` — Branch if SREG bit set
11. `BRCC` — Branch if Carry cleared
12. `BRCS` — Branch if Carry set
13. `BREAK` — Break
14. `BREQ` — Branch if Equal
15. `BRGE` — Branch if Greater or Equal, signed
16. `BRHC` — Branch if Half Carry cleared
17. `BRHS` — Branch if Half Carry set
18. `BRID` — Branch if Global Interrupt disabled
19. `BRIE` — Branch if Global Interrupt enabled
20. `BRLO` — Branch if Lower, unsigned
21. `BRLT` — Branch if Less Than, signed
22. `BRMI` — Branch if Minus
23. `BRNE` — Branch if Not Equal
24. `BRPL` — Branch if Plus
25. `BRSH` — Branch if Same or Higher, unsigned
26. `BRTC` — Branch if T cleared
27. `BRTS` — Branch if T set
28. `BRVC` — Branch if Overflow cleared
29. `BRVS` — Branch if Overflow set
30. `BSET` — Bit Set in SREG
31. `BST` — Bit Store from register bit to T
32. `CALL` — Long Call to Subroutine
33. `CBI` — Clear Bit in I/O Register
34. `CBR` — Clear Bits in Register
35. `CLC` — Clear Carry
36. `CLH` — Clear Half Carry
37. `CLI` — Clear Global Interrupt Enable
38. `CLN` — Clear Negative
39. `CLR` — Clear Register
40. `CLS` — Clear Sign
41. `CLT` — Clear T
42. `CLV` — Clear Overflow
43. `CLZ` — Clear Zero
44. `COM` — One's Complement
45. `CP` — Compare
46. `CPC` — Compare with Carry
47. `CPI` — Compare with Immediate
48. `CPSE` — Compare, Skip if Equal
49. `DEC` — Decrement
50. `DES` — Data Encryption Standard round
51. `EICALL` — Extended Indirect Call
52. `EIJMP` — Extended Indirect Jump
53. `ELPM` — Extended Load Program Memory
54. `EOR` — Exclusive OR
55. `FMUL` — Fractional Multiply Unsigned
56. `FMULS` — Fractional Multiply Signed
57. `FMULSU` — Fractional Multiply Signed × Unsigned
58. `ICALL` — Indirect Call
59. `IJMP` — Indirect Jump
60. `IN` — Load I/O Location to Register
61. `INC` — Increment
62. `JMP` — Jump
63. `LAC` — Load and Clear
64. `LAS` — Load and Set
65. `LAT` — Load and Toggle
66. `LD` using X — indirect load; plain, post-increment and pre-decrement forms
67. `LD` / `LDD` using Y — indirect/displacement load forms
68. `LD` / `LDD` using Z — indirect/displacement load forms
69. `LDI` — Load Immediate
70. `LDS` — Load Direct from Data Space, ordinary encoding
71. `LDS (AVRrc)` — reduced-core direct-load encoding
72. `LPM` — Load Program Memory; implicit-R0 and explicit-register/Z/Z+ forms where implemented
73. `LSL` — Logical Shift Left
74. `LSR` — Logical Shift Right
75. `MOV` — Copy Register
76. `MOVW` — Copy Register Word
77. `MUL` — Multiply Unsigned
78. `MULS` — Multiply Signed
79. `MULSU` — Multiply Signed × Unsigned
80. `NEG` — Two's Complement
81. `NOP` — No Operation
82. `OR` — Logical OR
83. `ORI` — Logical OR with Immediate
84. `OUT` — Store Register to I/O Location
85. `POP` — Pop Register
86. `PUSH` — Push Register
87. `RCALL` — Relative Call
88. `RET` — Return from Subroutine
89. `RETI` — Return from Interrupt
90. `RJMP` — Relative Jump
91. `ROL` — Rotate Left through Carry
92. `ROR` — Rotate Right through Carry
93. `SBC` — Subtract with Carry
94. `SBCI` — Subtract Immediate with Carry
95. `SBI` — Set Bit in I/O Register
96. `SBIC` — Skip if I/O Bit Cleared
97. `SBIS` — Skip if I/O Bit Set
98. `SBIW` — Subtract Immediate from Word
99. `SBR` — Set Bits in Register
100. `SBRC` — Skip if Register Bit Cleared
101. `SBRS` — Skip if Register Bit Set
102. `SEC` — Set Carry
103. `SEH` — Set Half Carry
104. `SEI` — Set Global Interrupt Enable
105. `SEN` — Set Negative
106. `SER` — Set All Bits in Register
107. `SES` — Set Sign
108. `SET` — Set T
109. `SEV` — Set Overflow
110. `SEZ` — Set Zero
111. `SLEEP` — Sleep
112. `SPM (AVRe)` — Store Program Memory, AVRe form
113. `SPM (AVRxm/AVRxt)` — Store Program Memory, newer-core form(s)
114. `ST` using X — indirect store; plain, post-increment and pre-decrement forms
115. `ST` / `STD` using Y — indirect/displacement store forms
116. `ST` / `STD` using Z — indirect/displacement store forms
117. `STS` — Store Direct to Data Space, ordinary encoding
118. `STS (AVRrc)` — reduced-core direct-store encoding
119. `SUB` — Subtract without Carry
120. `SUBI` — Subtract Immediate
121. `SWAP` — Swap Nibbles
122. `TST` — Test for Zero or Minus
123. `WDR` — Watchdog Reset
124. `XCH` — Exchange

## Core/version rule

Do not infer availability from the mnemonic list alone. `AVRrc` in particular removes instructions and changes direct-load/store encodings; newer tinyAVR parts use AVRxt. The machine-readable follow-up table must carry core availability per instruction/form.

Aliases/specializations such as `CLR`, `LSL`, `ROL`, `TST`, `CBR`, `SBR`, flag-set/clear spellings and conditional-branch spellings should preserve assembler-visible names while also recording their underlying encoding identity.

Idriç support is a separate column, never a filter on the architecture inventory.
