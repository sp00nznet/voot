#!/usr/bin/env python3
"""
ABI register save/restore address finder for Xbox 360 PPC binaries.
Finds the addresses of compiler-generated register save/restore helper
functions (e.g., _savegpr_14, _restgpr_14, _savefpr_14, etc.).

These are needed for correct function prologue/epilogue handling in
the static recompiler.
"""

import struct
import sys


# Known PPC instruction patterns for ABI helpers
# _savegpr_XX: stw rXX, offset(r1)
# _restgpr_XX: lwz rXX, offset(r1)
# _savefpr_XX: stfd fXX, offset(r1)
# _restfpr_XX: lfd fXX, offset(r1)

# PowerPC instruction encoding
def decode_ppc(word):
    opcode = (word >> 26) & 0x3F
    rs = (word >> 21) & 0x1F
    ra = (word >> 16) & 0x1F
    d = word & 0xFFFF
    if d >= 0x8000:
        d -= 0x10000
    return opcode, rs, ra, d


def find_abi_helpers(xex_path):
    with open(xex_path, 'rb') as f:
        data = f.read()

    if data[:4] != b'XEX2':
        print("ERROR: Not a valid XEX2 file")
        return

    pe_offset = struct.unpack_from('>I', data, 0x08)[0]
    base_address = 0x82000000

    # Parse headers for base address
    header_count = struct.unpack_from('>I', data, 0x14)[0]
    oh_offset = 0x18
    for h in range(header_count):
        if oh_offset + 8 > len(data):
            break
        header_id = struct.unpack_from('>I', data, oh_offset)[0]
        header_data = struct.unpack_from('>I', data, oh_offset + 4)[0]
        if header_id == 0x00010201:
            base_address = header_data
        oh_offset += 8

    pe_data = data[pe_offset:]

    print(f"Searching for ABI register save/restore helpers...")
    print(f"Image base: 0x{base_address:08X}")
    print(f"PE offset:  0x{pe_offset:X}")
    print(f"PE size:    0x{len(pe_data):X}")
    print()

    # Search for sequences of stw instructions with consecutive registers
    # Pattern: stw r14, -72(r1); stw r15, -68(r1); ... stw r31, -4(r1); blr
    # Opcode for stw: 36 (0x24)
    # Opcode for lwz: 32 (0x20)
    # Opcode for stfd: 54 (0x36)
    # Opcode for lfd: 50 (0x32)

    results = {
        'savegpr': {},
        'restgpr': {},
        'savefpr': {},
        'restfpr': {},
    }

    for offset in range(0, len(pe_data) - 80, 4):
        word = struct.unpack_from('>I', pe_data, offset)[0]
        opcode, rs, ra, d = decode_ppc(word)

        # Look for stw rXX, offset(r1) where XX is between 14 and 31
        if opcode == 36 and ra == 1 and 14 <= rs <= 31:  # stw rs, d(r1)
            # Check if this is the start of a save sequence
            reg_start = rs
            seq_len = 0
            for i in range(32 - reg_start):
                next_word = struct.unpack_from('>I', pe_data, offset + i * 4)[0]
                next_op, next_rs, next_ra, next_d = decode_ppc(next_word)
                if next_op == 36 and next_ra == 1 and next_rs == reg_start + i:
                    seq_len += 1
                else:
                    break

            if seq_len >= 2 and seq_len == (32 - reg_start):
                # Check for blr after the sequence
                after_word = struct.unpack_from('>I', pe_data, offset + seq_len * 4)[0]
                if after_word == 0x4E800020:  # blr
                    addr = base_address + pe_offset + offset
                    results['savegpr'][reg_start] = addr
                    print(f"  _savegpr_{reg_start}: 0x{addr:08X}")

        # Look for lwz rXX, offset(r1) sequences (restore)
        if opcode == 32 and ra == 1 and 14 <= rs <= 31:  # lwz rs, d(r1)
            reg_start = rs
            seq_len = 0
            for i in range(32 - reg_start):
                next_word = struct.unpack_from('>I', pe_data, offset + i * 4)[0]
                next_op, next_rs, next_ra, next_d = decode_ppc(next_word)
                if next_op == 32 and next_ra == 1 and next_rs == reg_start + i:
                    seq_len += 1
                else:
                    break

            if seq_len >= 2 and seq_len == (32 - reg_start):
                after_word = struct.unpack_from('>I', pe_data, offset + seq_len * 4)[0]
                if after_word == 0x4E800020:  # blr
                    addr = base_address + pe_offset + offset
                    results['restgpr'][reg_start] = addr
                    print(f"  _restgpr_{reg_start}: 0x{addr:08X}")

        # FPR save: stfd fXX, d(r1)
        if opcode == 54 and ra == 1 and 14 <= rs <= 31:  # stfd
            reg_start = rs
            seq_len = 0
            for i in range(32 - reg_start):
                next_word = struct.unpack_from('>I', pe_data, offset + i * 4)[0]
                next_op, next_rs, next_ra, next_d = decode_ppc(next_word)
                if next_op == 54 and next_ra == 1 and next_rs == reg_start + i:
                    seq_len += 1
                else:
                    break

            if seq_len >= 2 and seq_len == (32 - reg_start):
                after_word = struct.unpack_from('>I', pe_data, offset + seq_len * 4)[0]
                if after_word == 0x4E800020:
                    addr = base_address + pe_offset + offset
                    results['savefpr'][reg_start] = addr
                    print(f"  _savefpr_{reg_start}: 0x{addr:08X}")

        # FPR restore: lfd fXX, d(r1)
        if opcode == 50 and ra == 1 and 14 <= rs <= 31:  # lfd
            reg_start = rs
            seq_len = 0
            for i in range(32 - reg_start):
                next_word = struct.unpack_from('>I', pe_data, offset + i * 4)[0]
                next_op, next_rs, next_ra, next_d = decode_ppc(next_word)
                if next_op == 50 and next_ra == 1 and next_rs == reg_start + i:
                    seq_len += 1
                else:
                    break

            if seq_len >= 2 and seq_len == (32 - reg_start):
                after_word = struct.unpack_from('>I', pe_data, offset + seq_len * 4)[0]
                if after_word == 0x4E800020:
                    addr = base_address + pe_offset + offset
                    results['restfpr'][reg_start] = addr
                    print(f"  _restfpr_{reg_start}: 0x{addr:08X}")

    print(f"\nFound: {sum(len(v) for v in results.values())} ABI helper functions")
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <xex_file>")
        sys.exit(1)
    find_abi_helpers(sys.argv[1])
