# Virtual On: Oratorio Tangram - Binary Analysis

## XEX Binary Details

| Property | Value |
|---|---|
| Title | Virtual On: Oratorio Tangram |
| Title ID | `0x58410985` |
| Format | XEX2 (XBLA) |
| Architecture | PowerPC (Xenon, big-endian) |
| Image Base | `0x82000000` |
| Image Size | `0x1A30000` (26.2 MB) |
| PE Offset | `0x4000` |
| Entry Point | `0x00000604` (relative) |
| Module Flags | `0x00000001` |
| SHA1 Hash | `f8d7ec5163cdb20ff3870b83885c8dd82fafdbb2` |

## Imports

The game imports from two Xbox 360 system libraries:

### xboxkrnl.exe
Core kernel functions: threading, memory, file I/O, synchronization.

### xam.xex
Xbox Application Manager: user profiles, achievements, marketplace, UI.

## STFS Container

| Property | Value |
|---|---|
| Magic | `LIVE` |
| Content Type | `0x000D0000` (Xbox Marketplace Content) |
| Display Name | Virtual-On OT |
| Container Size | 228.8 MB |

## PE Sections (TBD)

Will be populated after first recompilation pass:
- Code section bounds
- Data section bounds
- BSS section
- Resource sections

## Function Analysis (TBD)

Will be populated after codegen:
- Total functions recompiled
- Manual overrides needed
- Switch tables discovered
- ABI helper locations

## Game Engine Notes

Virtual On: Oratorio Tangram was originally a SEGA arcade game (NAOMI hardware),
later ported to Dreamcast, and then to Xbox 360 as an XBLA title by Hitmaker/SEGA.

The Xbox 360 version is a full port with HD graphics, online multiplayer, and
achievements. The game engine likely shares lineage with other SEGA arcade
frameworks of the era.

### Known Game Subsystems (to be mapped during recomp)
- Mech (Virtuaroid) management and AI
- Physics / collision detection
- 3D rendering pipeline
- Animation system
- Sound / music system
- Input handling (twin stick controls)
- Network / multiplayer
- Save data
- Achievement tracking
