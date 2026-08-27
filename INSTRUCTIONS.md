# AURIX / TriCore complete instruction inventory

Status: source-backed architecture inventory. `AURIX` is a product family, not one invariant ISA.

## Generation split

### AURIX TC3xx

CPU architecture: **TriCore TC1.6.2P**.

Normative instruction source: Infineon **TriCore TC1.6.2 core architecture manual, Instruction Set, Volume 2**, V1.2.2 / 2020-01-15. Infineon describes this volume as the complete TriCore instruction-set description including optional MMU/FPU extensions. TC3xx product documentation identifies its CPUs as TC1.6.2P implementations.

### AURIX TC4xx

CPU architecture: **TriCore TC1.8**.

Normative instruction source: Infineon **TriCore TC1.8 architecture manual volume 2**, V1.0.0 / 2024-02-14. The manual states that Volume 2 gives a complete description of the TriCore instruction set including optional MMU/FPU extensions. TC4xx documentation identifies its CPU as a TC1.8 implementation and notes that TC1.8 adds virtualization and double-precision IEEE-754-2019 floating point relative to TC1.6.

TC4xx product documentation also states that the optional MMU is not implemented in that product family. Architecture inventory and product availability therefore remain separate columns.

## Exhaustive extraction rule

Both Infineon Volume-2 manuals organize each documented machine instruction as a numbered Chapter-3 subsection (`3.1.n`, then extension groups such as floating-point and virtualization). Their tables of contents repeat those section numbers and mnemonics.

`tools/extract-manual-instructions.py PDF` uses `pdftotext -layout` and independently extracts:

1. every numbered instruction entry from the table of contents;
2. every matching numbered instruction heading from the body;
3. the mnemonic and section number for each.

Generation **fails unless the TOC set and body set are identical**. This gives a useful completeness oracle without hand-copying hundreds of instructions.

The output is TSV in section order and can be augmented later with syntax/opcode/status/privilege fields from each instruction page. The canonical PDF remains the semantic/encoding authority.

## Independent TC1.6.2 execution/encoding cross-check

QEMU's TriCore target at commit `bbc8fb89fa3478a6f47c0475d2e4952e69a64f45` contains `target/tricore/tricore-opcodes.h`, including enumerated 16-bit and 32-bit opcode/form constants used by its TC1.6.2 implementation. This is useful as an executable cross-check, not a substitute for Infineon's complete manual.

## No family flattening

Do not merge TC1.6.2P and TC1.8 into one unversioned mnemonic list. The branch should generate two inventories and then compare them explicitly:

- shared instructions/forms;
- TC1.6.2P-only or implementation-specific forms;
- TC1.8 additions/changes;
- product-unimplemented optional facilities.

Idriç support remains a separate matrix from both complete inventories.
