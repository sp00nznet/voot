#!/usr/bin/env python3
"""
Post-codegen fixup for Virtual On: Oratorio Tangram.
Re-applies safety macro overrides to the generated voot_init.h after codegen
regenerates it. This is necessary because codegen overwrites the header.

Run this after every `rexglue.exe codegen` pass.
"""

import sys
from pathlib import Path

INIT_HEADER = Path(__file__).parent.parent / "generated" / "voot_init.h"

SAFETY_OVERRIDES = '''
// ============================================================================
// Safety Macro Overrides (re-applied by post_codegen.py)
// ============================================================================
#include "voot_config.h"

// Safe indirect function call dispatch
#ifdef PPC_CALL_INDIRECT_FUNC
#undef PPC_CALL_INDIRECT_FUNC
#endif
#define PPC_CALL_INDIRECT_FUNC(ctx, target) \\
    do { \\
        if ((target) == 0) { \\
            ctx.r3.u64 = 0; \\
            break; \\
        } \\
        if ((target) < VOOT_CODE_START || (target) >= VOOT_CODE_END) { \\
            ctx.r3.u64 = 0; \\
            break; \\
        } \\
        auto* __fn = PPCFuncTable::getFunc(target); \\
        if (__fn == nullptr) { \\
            ctx.r3.u64 = 0; \\
            break; \\
        } \\
        __fn(ctx, target); \\
    } while(0)

// Unimplemented PPC instruction handler (warn, don't crash)
#ifdef PPC_UNIMPLEMENTED
#undef PPC_UNIMPLEMENTED
#endif
#define PPC_UNIMPLEMENTED(ctx, addr, opcode) \\
    do { \\
        static bool __warned = false; \\
        if (!__warned) { \\
            printf("[VOOT] WARNING: Unimplemented PPC instruction at 0x%08X (opcode: 0x%08X)\\n", \\
                   (unsigned)(addr), (unsigned)(opcode)); \\
            __warned = true; \\
        } \\
    } while(0)

// ============================================================================
'''


def main():
    if not INIT_HEADER.exists():
        print(f"ERROR: {INIT_HEADER} not found. Run codegen first.")
        sys.exit(1)

    content = INIT_HEADER.read_text(encoding='utf-8')

    # Check if overrides are already present
    if 'Safety Macro Overrides (re-applied by post_codegen.py)' in content:
        print("Safety overrides already present. Skipping.")
        return

    # Find the #pragma once line and insert overrides after it
    if '#pragma once' in content:
        content = content.replace('#pragma once', '#pragma once\n' + SAFETY_OVERRIDES, 1)
    else:
        content = SAFETY_OVERRIDES + '\n' + content

    INIT_HEADER.write_text(content, encoding='utf-8')
    print(f"Safety overrides applied to {INIT_HEADER}")
    print("  - PPC_CALL_INDIRECT_FUNC: NULL check + range validation + slot check")
    print("  - PPC_UNIMPLEMENTED: warn-and-skip (no crash)")


if __name__ == '__main__':
    main()
