# VOOT - Virtual On: Oratorio Tangram (Xbox 360) Static Recompilation

```
  ██╗   ██╗ ██████╗  ██████╗ ████████╗
  ██║   ██║██╔═══██╗██╔═══██╗╚══██╔══╝
  ██║   ██║██║   ██║██║   ██║   ██║
  ╚██╗ ██╔╝██║   ██║██║   ██║   ██║
   ╚████╔╝ ╚██████╔╝╚██████╔╝   ██║
    ╚═══╝   ╚═════╝  ╚═════╝    ╚═╝
    VIRTUAL-ON ORATORIO TANGRAM
         NATIVE PC RECOMP
```

> *"In the year 2025, humanity's greatest virtual warriors return —
> this time running natively on your PC at full speed, no emulator required."*

## What Is This?

This is a **static recompilation** of **Virtual On: Oratorio Tangram** (Xbox 360 / XBLA) to native x86-64 Windows. The entire Xbox 360 PowerPC binary is translated ahead-of-time into C++ source code, then compiled into a native Windows executable.

**No emulator. No interpreter. No JIT. Pure native speed.**

The legendary mech-on-mech arena combat game, ripped straight from the Xenon silicon and rebuilt for modern hardware.

## How It Works

```
  ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
  │  default.xex │────>│  XenonRecomp  │────>│  Generated   │
  │  (PPC binary)│     │  + ReXGlue    │     │  C++ Source  │
  └──────────────┘     └───────────────┘     └──────┬───────┘
                                                     │
  ┌──────────────┐     ┌───────────────┐            │
  │   voot.exe   │<────│  Clang 18+    │<───────────┘
  │  (native!)   │     │  + ReXGlue SDK│   + hand-written
  └──────────────┘     └───────────────┘     project code
```

1. **XenonRecomp** (via ReXGlue) reads the Xbox 360 XEX binary and translates all PowerPC functions into C++ code
2. Hand-written project code provides the runtime glue: Xbox 360 kernel stubs, GPU translation (D3D12), audio, input, and game-specific fixes
3. Everything compiles with **Clang 18+** into a native Win32 executable
4. The **ReXGlue SDK** provides the full Xbox 360 runtime environment: kernel emulation, D3D12-based GPU backend (translated from Xenos), XMA audio, and more

## Tech Stack

| Component | Technology |
|---|---|
| Recompiler | [XenonRecomp](https://github.com/hedge-dev/XenonRecomp) |
| Runtime SDK | [ReXGlue SDK](https://github.com/hedge-dev/ReXGlue) |
| GPU Backend | D3D12 (Xenia-derived shader translation) |
| Compiler | Clang 18+ (clang-cl) |
| Build System | CMake 3.25+ / Ninja |
| UI Overlay | ImGui |
| Input | SDL2 |
| Audio | XMA decode (ReXGlue) |

## Binary Details

| Property | Value |
|---|---|
| Title | Virtual On: Oratorio Tangram |
| Title ID | `0x58410985` |
| Platform | Xbox 360 (XBLA) |
| Architecture | PowerPC (Xenon, big-endian) |
| Image Base | `0x82000000` |
| Image Size | `0x1A30000` (~26.2 MB) |
| PE Offset | `0x4000` |
| Imports | `xboxkrnl.exe`, `xam.xex` |

## Building

### Prerequisites

- **CMake 3.25+**
- **Clang 18+** (`clang-cl`)
- **Ninja** build system
- **ReXGlue SDK** (follow setup at https://github.com/hedge-dev/ReXGlue)
- **Python 3.10+** (for tools)
- Windows 10/11 with D3D12 support (ROV-capable GPU recommended)

### Step 1: Code Generation

Place your legally obtained `default.xex` in the project root, then run:

```bash
rexglue.exe codegen --config config/voot_rexglue.toml
```

This generates the recompiled C++ source files in `generated/`.

### Step 2: Post-Codegen Fixup

```bash
python tools/post_codegen.py
```

Applies safety macro overrides to the generated init header.

### Step 3: Build

```bash
cmake -S project -B build -G Ninja -DCMAKE_C_COMPILER=clang-cl -DCMAKE_CXX_COMPILER=clang-cl
cmake --build build --config Release
```

### Step 4: Run

```bash
./build/voot.exe
```

Grab your twin sticks. It's Tangram time.

## Project Structure

```
voot/
├── config/
│   ├── voot_rexglue.toml        # ReXGlue codegen configuration
│   └── voot_switch_tables.toml  # Jump table definitions
├── generated/
│   ├── voot_config.h            # Address constants
│   ├── voot_init.h              # Function declarations + safety overrides
│   ├── voot_init.cpp            # Function table
│   └── sources.cmake            # Generated source file list
├── project/
│   ├── CMakeLists.txt           # Build system
│   └── src/
│       ├── main.cpp             # VootApp entry point, VEH handlers
│       ├── stubs.cpp            # Xbox 360 API stubs
│       ├── menu.cpp/h           # Native menu system
│       └── settings.cpp/h       # TOML settings persistence
├── tools/
│   ├── extract_stfs.py          # STFS package extractor
│   ├── extract_xex_direct.py    # XEX binary extractor
│   ├── xex_info.py              # XEX header analysis
│   ├── find_missing_vtable_funcs.py  # Vtable scanner
│   └── post_codegen.py          # Post-codegen fixup script
├── docs/
│   └── binary-analysis.md       # XEX binary details & notes
└── README.md                    # You are here
```

## Progress

### Current Status: Phase 1 - Foundation

- [x] STFS package extraction
- [x] XEX binary extraction and analysis
- [x] Project structure and build system
- [x] ReXGlue codegen configuration
- [x] Core source files (main, stubs, generated headers)
- [x] Helper tools (STFS extractor, XEX analyzer, vtable scanner)
- [ ] First recompilation pass (codegen)
- [ ] Clean compile (0 errors)
- [ ] Runtime skeleton (window, file I/O)
- [ ] Game boot sequence
- [ ] GPU initialization
- [ ] First rendered frame
- [ ] Full gameplay

### Builds On

This project builds directly on the architecture and patterns established by [vig8](https://github.com/sp00nznet/vig8) (Vigilante 8 Arcade static recompilation). Key patterns carried over:

- Safe indirect call dispatch (`PPC_CALL_INDIRECT_FUNC` override)
- VEH null page handler for guest memory access violations
- Weak function override pattern for game-specific stubs
- ReXGlue SDK integration workflow
- Iterative crash-debug-fix development cycle

## Legal

This project contains no copyrighted game code or assets. You must provide your own legally obtained copy of Virtual On: Oratorio Tangram (Xbox 360) to use this recompiler.

The recompilation tools and runtime code are open source. The generated C++ source (from your own binary) is gitignored.

## Credits

- **[hedge-dev](https://github.com/hedge-dev)** - XenonRecomp and ReXGlue SDK
- **Xenia Project** - D3D12 GPU backend heritage
- **SEGA / Hitmaker** - Virtual On: Oratorio Tangram (original game)
- **sp00nznet** - This recompilation project

---

*Get in the Virtuaroid. We're going home.*
