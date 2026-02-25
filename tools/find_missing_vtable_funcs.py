#!/usr/bin/env python3
"""
Vtable function scanner for Virtual On: Oratorio Tangram.
Scans the PE data section for addresses that look like vtable entries
and checks if they're present in the recompiled function table.

This catches functions that the static recompiler missed because they're
only called through vtable dispatch (indirect calls), not direct calls.
"""

import struct
import sys
import re
from pathlib import Path


def scan_vtable_entries(xex_path, func_table_path=None):
    """Scan XEX data section for potential vtable entries."""
    with open(xex_path, 'rb') as f:
        data = f.read()

    if data[:4] != b'XEX2':
        print("ERROR: Not a valid XEX2 file")
        return

    pe_offset = struct.unpack_from('>I', data, 0x08)[0]
    security_offset = struct.unpack_from('>I', data, 0x10)[0]
    image_size = struct.unpack_from('>I', data, security_offset + 4)[0]

    # Get image base from optional headers
    header_count = struct.unpack_from('>I', data, 0x14)[0]
    base_address = 0x82000000  # default
    oh_offset = 0x18
    for h in range(header_count):
        if oh_offset + 8 > len(data):
            break
        header_id = struct.unpack_from('>I', data, oh_offset)[0]
        header_data = struct.unpack_from('>I', data, oh_offset + 4)[0]
        if header_id == 0x00010201:  # IMAGE_BASE_ADDRESS
            base_address = header_data
        oh_offset += 8

    code_start = base_address + pe_offset
    code_end = base_address + image_size

    print(f"Image base:  0x{base_address:08X}")
    print(f"Code range:  0x{code_start:08X} - 0x{code_end:08X}")
    print(f"Image size:  0x{image_size:X}")

    # Load known function addresses from function table (if available)
    known_funcs = set()
    if func_table_path and Path(func_table_path).exists():
        with open(func_table_path, 'r') as f:
            for line in f:
                # Match patterns like: { 0x82010000, sub_82010000, "sub_82010000" },
                match = re.search(r'0x([0-9A-Fa-f]{8})', line)
                if match:
                    addr = int(match.group(1), 16)
                    if code_start <= addr < code_end:
                        known_funcs.add(addr)

        print(f"Known functions: {len(known_funcs)}")

    # Scan PE data for potential vtable entries
    # Vtables are arrays of function pointers in the data section
    # On Xbox 360 (big-endian), these are 4-byte addresses pointing into the code section

    pe_data = data[pe_offset:]
    potential_vtable_entries = set()
    consecutive_runs = []
    current_run = []

    for offset in range(0, len(pe_data) - 4, 4):
        # Read as big-endian 32-bit
        val = struct.unpack_from('>I', pe_data, offset)[0]

        # Check if this looks like a code address
        if code_start <= val < code_end:
            # Addresses should be 4-byte aligned (PPC instructions are 4 bytes)
            if val % 4 == 0:
                potential_vtable_entries.add(val)
                current_run.append((base_address + pe_offset + offset, val))
        else:
            if len(current_run) >= 3:  # At least 3 consecutive code pointers = likely vtable
                consecutive_runs.append(current_run[:])
            current_run = []

    if len(current_run) >= 3:
        consecutive_runs.append(current_run)

    print(f"\nPotential vtable function addresses: {len(potential_vtable_entries)}")
    print(f"Consecutive pointer runs (likely vtables): {len(consecutive_runs)}")

    # Find addresses NOT in the known function table
    if known_funcs:
        missing = potential_vtable_entries - known_funcs
        print(f"\nMissing from function table: {len(missing)}")
        if missing:
            print("\nMissing vtable function addresses:")
            for addr in sorted(missing):
                print(f"  0x{addr:08X}")
    else:
        print(f"\nAll potential vtable entries (run with --func-table to filter):")
        for addr in sorted(potential_vtable_entries)[:50]:
            print(f"  0x{addr:08X}")
        if len(potential_vtable_entries) > 50:
            print(f"  ... and {len(potential_vtable_entries) - 50} more")

    # Show vtable clusters
    if consecutive_runs:
        print(f"\nLargest vtable clusters:")
        consecutive_runs.sort(key=lambda r: len(r), reverse=True)
        for i, run in enumerate(consecutive_runs[:10]):
            data_addr = run[0][0]
            print(f"  [{i}] at 0x{data_addr:08X}: {len(run)} entries")
            for loc, target in run[:5]:
                marker = " (MISSING)" if known_funcs and target not in known_funcs else ""
                print(f"       0x{loc:08X} -> 0x{target:08X}{marker}")
            if len(run) > 5:
                print(f"       ... and {len(run) - 5} more")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <xex_file> [--func-table <init.cpp>]")
        sys.exit(1)

    func_table = None
    if '--func-table' in sys.argv:
        idx = sys.argv.index('--func-table')
        if idx + 1 < len(sys.argv):
            func_table = sys.argv[idx + 1]

    scan_vtable_entries(sys.argv[1], func_table)
