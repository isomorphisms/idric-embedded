#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def read_uleb(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while True:
        if offset >= len(data):
            raise AssertionError("truncated ULEB")
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if byte < 0x80:
            return value, offset
        shift += 7
        if shift > 35:
            raise AssertionError("oversized ULEB in first-slice module")


def sections(data: bytes) -> list[tuple[int, bytes]]:
    if data[:8] != b"\x00asm\x01\x00\x00\x00":
        raise AssertionError("wrong WebAssembly magic/version preamble")
    out: list[tuple[int, bytes]] = []
    offset = 8
    while offset < len(data):
        section_id = data[offset]
        offset += 1
        size, offset = read_uleb(data, offset)
        end = offset + size
        if end > len(data):
            raise AssertionError("section extends past end of module")
        out.append((section_id, data[offset:end]))
        offset = end
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("module", type=Path)
    parser.add_argument("--export", default="idric_answer")
    parser.add_argument("--value", type=int, default=42)
    args = parser.parse_args()

    data = args.module.read_bytes()
    found = sections(data)
    ids = [section_id for section_id, _ in found]
    if ids != [1, 3, 7, 10]:
        raise AssertionError(
            f"first slice must contain only type/function/export/code sections, got {ids}"
        )

    type_payload = found[0][1]
    if type_payload != bytes([1, 0x60, 0, 1, 0x7F]):
        raise AssertionError(f"unexpected type section: {type_payload.hex()}")

    if found[1][1] != bytes([1, 0]):
        raise AssertionError("function section is not one function at type index zero")

    export_payload = found[2][1]
    offset = 0
    count, offset = read_uleb(export_payload, offset)
    if count != 1:
        raise AssertionError("expected exactly one export")
    name_len, offset = read_uleb(export_payload, offset)
    name = export_payload[offset : offset + name_len].decode("ascii")
    offset += name_len
    if name != args.export:
        raise AssertionError(f"unexpected export name {name!r}")
    if export_payload[offset:] != bytes([0, 0]):
        raise AssertionError("export must be function index zero")

    code_payload = found[3][1]
    offset = 0
    count, offset = read_uleb(code_payload, offset)
    if count != 1:
        raise AssertionError("expected exactly one code body")
    body_len, offset = read_uleb(code_payload, offset)
    body = code_payload[offset : offset + body_len]
    if offset + body_len != len(code_payload):
        raise AssertionError("unexpected trailing code-section bytes")
    expected = bytes([0, 0x41, args.value & 0x7F, 0x0B])
    if not (0 <= args.value <= 63):
        raise AssertionError("shape oracle currently assumes one-byte positive SLEB")
    if body != expected:
        raise AssertionError(
            f"expected locals=0; i32.const {args.value}; end, got {body.hex()}"
        )


if __name__ == "__main__":
    main()
