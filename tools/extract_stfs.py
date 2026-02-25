#!/usr/bin/env python3
"""
STFS (Xbox 360 LIVE/PIRS/CON) package extractor.
Extracts files from Xbox 360 marketplace packages to find default.xex.
Based on the STFS format specification.
"""

import struct
import sys
import os
from pathlib import Path


def read_utf16be(data, offset, max_len):
    """Read a UTF-16 BE string from data."""
    raw = data[offset:offset + max_len * 2]
    try:
        return raw.decode('utf-16-be').rstrip('\x00')
    except:
        return ""


def compute_data_block_offset(block_num, header_size):
    """Compute the file offset for a given data block number."""
    # Each block is 0x1000 bytes
    # Need to account for hash table blocks interspersed in the data
    BLOCK_SIZE = 0x1000

    # Determine which hash table blocks to skip
    # Level 0 hash tables: one per 0xAA data blocks
    # Level 1 hash tables: one per 0xAA L0 hash tables
    # Level 2 hash tables: one per 0xAA L1 hash tables

    num_l0_tables = block_num // 0xAA
    if block_num % 0xAA > 0 or block_num == 0:
        pass  # no extra

    # Simplified: compute actual block index accounting for hash tables
    actual_block = block_num
    # Add L0 hash table blocks
    actual_block += (block_num + 0xA9) // 0xAA
    # Add L1 hash table blocks
    l0_count = (block_num + 0xA9) // 0xAA
    actual_block += (l0_count + 0xA9) // 0xAA

    return header_size + actual_block * BLOCK_SIZE


def extract_stfs(stfs_path, output_dir):
    """Extract all files from an STFS package."""
    with open(stfs_path, 'rb') as f:
        data = f.read()

    magic = data[0:4]
    magic_str = magic.decode('ascii', errors='replace')
    print(f"Magic: {magic_str}")

    if magic_str not in ('CON ', 'LIVE', 'PIRS'):
        print(f"ERROR: Not an STFS package (magic: {magic_str})")
        return False

    # Content type at offset 0x344
    content_type = struct.unpack_from('>I', data, 0x344)[0]
    print(f"Content Type: 0x{content_type:08X}")

    # Title ID at offset 0x360
    title_id = struct.unpack_from('>I', data, 0x360)[0]
    print(f"Title ID: 0x{title_id:08X}")

    # Display name (UTF-16 BE) at offset 0x411
    display_name = read_utf16be(data, 0x411, 128)
    print(f"Display Name: {display_name}")

    # Description at offset 0x611
    description = read_utf16be(data, 0x611, 128)
    if description:
        print(f"Description: {description}")

    # Volume descriptor at 0x379
    # STFS descriptor starts at 0x379
    vol_type = data[0x379]  # 0 = STFS, 1 = SVOD

    # STFS volume descriptor
    stfs_desc_offset = 0x379

    # Header size depends on magic
    if magic_str == 'CON ':
        header_size = 0xB000
    else:
        header_size = 0xA000  # LIVE/PIRS typically 0xA000, but can vary

    # File table block number at 0x37E (within volume descriptor)
    # Volume descriptor layout:
    #   0x379: descriptor size (1 byte)
    #   0x37A: reserved (1 byte)
    #   0x37B: block separation (1 byte)
    #   0x37C-0x37D: file table block count (2 bytes, BE)
    #   0x37E-0x380: file table block number (3 bytes, BE)

    desc_size = data[0x379]
    block_separation = data[0x37B]
    file_table_block_count = struct.unpack_from('>H', data, 0x37C)[0]

    # 3-byte big-endian block number
    ftb0 = data[0x37E]
    ftb1 = data[0x37F]
    ftb2 = data[0x380]
    file_table_block = (ftb0 << 16) | (ftb1 << 8) | ftb2

    # Total allocated block count at 0x381-0x383 (3 bytes BE)
    tab0 = data[0x381]
    tab1 = data[0x382]
    tab2 = data[0x383]
    total_alloc_blocks = (tab0 << 16) | (tab1 << 8) | tab2

    # Total unallocated block count at 0x384-0x386 (3 bytes BE)

    print(f"\nVolume Descriptor:")
    print(f"  Descriptor size: {desc_size}")
    print(f"  Block separation: {block_separation}")
    print(f"  File table block count: {file_table_block_count}")
    print(f"  File table start block: {file_table_block}")
    print(f"  Total allocated blocks: {total_alloc_blocks}")

    # Alternative header size: check if data at 0xA000 or 0xB000 looks like block data
    # Try to auto-detect
    for hs in [0xA000, 0xB000, 0xC000]:
        if hs < len(data):
            test_offset = hs
            # First block should be hash table or data
            print(f"  Testing header_size=0x{hs:X}: first bytes at offset = {data[test_offset:test_offset+4].hex()}")

    # Read file table
    BLOCK_SIZE = 0x1000
    ENTRY_SIZE = 0x40

    print(f"\nReading file table...")

    # For LIVE packages, use simpler block chain following
    # Read the file table by following block chain from the hash tables
    # For now, try direct block calculation

    # Collect file table data
    file_table_data = bytearray()

    # Try multiple header sizes and pick the one that works
    best_header = None
    for try_header in [0xA000, 0xB000, 0xC000]:
        # Simple approach: read file table blocks sequentially starting from file_table_block
        test_offset = try_header + file_table_block * BLOCK_SIZE
        if test_offset + BLOCK_SIZE <= len(data):
            # Check if this looks like a file listing (first entry should have readable name)
            test_entry = data[test_offset:test_offset + 0x40]
            name_len = test_entry[0x28]
            if 0 < name_len <= 0x28:
                name = test_entry[0:name_len].decode('ascii', errors='replace')
                if name.isprintable():
                    best_header = try_header
                    print(f"  Found valid file table at header_size=0x{try_header:X}, first entry name: '{name}'")
                    break

    if best_header is None:
        # Try with hash table interleaving
        for try_header in [0xA000, 0xB000, 0xC000]:
            offset = compute_data_block_offset(file_table_block, try_header)
            if offset + BLOCK_SIZE <= len(data):
                test_entry = data[offset:offset + 0x40]
                name_len = test_entry[0x28]
                if 0 < name_len <= 0x28:
                    name = test_entry[0:name_len].decode('ascii', errors='replace')
                    if name.isprintable():
                        best_header = try_header
                        print(f"  Found valid file table (with hash interleave) at header_size=0x{try_header:X}, first entry name: '{name}'")
                        break

    if best_header is None:
        print("ERROR: Could not locate file table. Trying brute force search for 'default.xex'...")
        # Brute force: search for XEX2 magic in the data
        xex_offsets = []
        search = b'XEX2'
        pos = 0
        while pos < len(data):
            idx = data.find(search, pos)
            if idx == -1:
                break
            xex_offsets.append(idx)
            pos = idx + 1

        if xex_offsets:
            print(f"  Found {len(xex_offsets)} XEX2 magic(s) at offsets: {[f'0x{o:X}' for o in xex_offsets]}")
            # Try to extract from the first one
            for xex_off in xex_offsets:
                print(f"\n  Attempting extraction from offset 0x{xex_off:X}...")
                # XEX header: magic (4) + flags (4) + PE offset (4) + ...
                # The PE data offset tells us the size
                if xex_off + 0x18 < len(data):
                    pe_offset = struct.unpack_from('>I', data, xex_off + 0x8)[0]
                    security_offset = struct.unpack_from('>I', data, xex_off + 0xC)[0]
                    header_count = struct.unpack_from('>I', data, xex_off + 0x14)[0]
                    print(f"    PE data offset: 0x{pe_offset:X}")
                    print(f"    Security offset: 0x{security_offset:X}")
                    print(f"    Header count: {header_count}")
        return False

    header_size = best_header

    # Read file table blocks (try simple sequential first, then with hash interleaving)
    file_entries = []

    # Try simple sequential reading
    for block_idx in range(file_table_block_count):
        block_num = file_table_block + block_idx

        # Try simple offset first
        offset = header_size + block_num * BLOCK_SIZE
        if offset + BLOCK_SIZE > len(data):
            # Try with hash interleaving
            offset = compute_data_block_offset(block_num, header_size)

        if offset + BLOCK_SIZE <= len(data):
            file_table_data.extend(data[offset:offset + BLOCK_SIZE])

    # Parse file entries
    num_entries = len(file_table_data) // ENTRY_SIZE
    print(f"  Parsing {num_entries} potential file entries...")

    # Directory map for path reconstruction
    directories = {0xFFFF: ""}  # Root

    for i in range(num_entries):
        entry_offset = i * ENTRY_SIZE
        entry = file_table_data[entry_offset:entry_offset + ENTRY_SIZE]

        name_len = entry[0x28]
        if name_len == 0:
            continue

        name_len_val = name_len & 0x3F
        if name_len_val == 0 or name_len_val > 0x28:
            continue

        name = entry[0:name_len_val].decode('ascii', errors='replace')
        if not name.isprintable():
            continue

        # Flags
        flags = entry[0x28] >> 6  # Top 2 bits of name_length byte

        # Sizes
        valid_data_blocks = struct.unpack_from('>I', data[0:4] if len(entry) < 0x2C + 4 else entry, 0x29)[0] if entry_offset + 0x2D <= len(file_table_data) else 0
        # Actually the layout is:
        # 0x00-0x27: filename (40 bytes)
        # 0x28: name_length (bottom 6 bits) + flags (top 2 bits)
        # 0x29-0x2B: valid data blocks (3 bytes BE)
        # 0x2C-0x2E: allocated data blocks (3 bytes BE)
        # 0x2F-0x31: first data block (3 bytes BE)
        # 0x32-0x33: path indicator (2 bytes BE) - index of parent dir
        # 0x34-0x37: file size (4 bytes BE)
        # 0x38-0x3B: update timestamp
        # 0x3C-0x3F: access timestamp

        vdb = (entry[0x29] << 16) | (entry[0x2A] << 8) | entry[0x2B]
        adb = (entry[0x2C] << 16) | (entry[0x2D] << 8) | entry[0x2E]
        first_block = (entry[0x2F] << 16) | (entry[0x30] << 8) | entry[0x31]
        path_indicator = struct.unpack_from('>H', entry, 0x32)[0]
        file_size = struct.unpack_from('>I', entry, 0x34)[0]

        is_dir = (entry[0x28] & 0x80) != 0
        is_blocks_consecutive = (entry[0x28] & 0x40) != 0

        if is_dir:
            directories[i] = name

        # Reconstruct path
        parent_path = directories.get(path_indicator, "")
        if parent_path:
            full_path = f"{parent_path}/{name}"
        else:
            full_path = name

        if is_dir:
            directories[i] = full_path

        entry_info = {
            'name': name,
            'full_path': full_path,
            'is_dir': is_dir,
            'consecutive': is_blocks_consecutive,
            'first_block': first_block,
            'valid_blocks': vdb,
            'alloc_blocks': adb,
            'file_size': file_size,
            'path_indicator': path_indicator,
        }
        file_entries.append(entry_info)

        type_str = "DIR " if is_dir else "FILE"
        print(f"  [{type_str}] {full_path} (size={file_size}, first_block={first_block}, blocks={vdb})")

    # Extract files
    os.makedirs(output_dir, exist_ok=True)
    extracted = 0

    for entry in file_entries:
        if entry['is_dir']:
            dir_path = os.path.join(output_dir, entry['full_path'].replace('/', os.sep))
            os.makedirs(dir_path, exist_ok=True)
            continue

        file_path = os.path.join(output_dir, entry['full_path'].replace('/', os.sep))
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        file_data = bytearray()
        remaining = entry['file_size']

        if entry['consecutive']:
            # Blocks are consecutive - simple sequential read
            block = entry['first_block']
            while remaining > 0:
                offset = header_size + block * BLOCK_SIZE
                if offset + BLOCK_SIZE > len(data):
                    offset = compute_data_block_offset(block, header_size)

                if offset + BLOCK_SIZE > len(data):
                    print(f"  WARNING: Block {block} out of range for {entry['name']}")
                    break

                chunk_size = min(BLOCK_SIZE, remaining)
                file_data.extend(data[offset:offset + chunk_size])
                remaining -= chunk_size
                block += 1
        else:
            # Need to follow block chain via hash tables
            # For now try consecutive as fallback
            block = entry['first_block']
            while remaining > 0:
                offset = header_size + block * BLOCK_SIZE
                if offset + BLOCK_SIZE > len(data):
                    offset = compute_data_block_offset(block, header_size)

                if offset + BLOCK_SIZE > len(data):
                    break

                chunk_size = min(BLOCK_SIZE, remaining)
                file_data.extend(data[offset:offset + chunk_size])
                remaining -= chunk_size
                block += 1

        with open(file_path, 'wb') as out_f:
            out_f.write(file_data[:entry['file_size']])

        extracted += 1
        print(f"  Extracted: {entry['full_path']} ({entry['file_size']} bytes)")

    print(f"\nExtracted {extracted} files to {output_dir}")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <stfs_file> <output_dir>")
        sys.exit(1)

    extract_stfs(sys.argv[1], sys.argv[2])
