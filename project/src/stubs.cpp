// Virtual On: Oratorio Tangram - Xbox 360 API Stubs
// Provides stub implementations for Xbox 360 APIs that the game imports
// but aren't needed (or need modification) for the PC recompilation.
//
// Functions declared as PPC_WEAK_FUNC in the generated code can be overridden
// here with strong definitions. This is the primary mechanism for intercepting
// and modifying game behavior without touching generated code.

#include <cstdio>
#include <cstring>

#include "voot_config.h"
// #include <rex/runtime/context.h>
// #include <rex/kernel/kernel.h>

// ============================================================================
// Networking Stubs
// ============================================================================
// VOOT has Xbox LIVE multiplayer, but we don't need it for single-player.
// These stubs return failure/no-op values so the game skips network init.

// XNetStartup - Network initialization
// PPC_FUNC void stub_XNetStartup(PPCContext& ctx, uint32_t addr) {
//     printf("[VOOT] STUB: XNetStartup() -> 0 (success, but no-op)\n");
//     ctx.r3.u64 = 0;  // Return SUCCESS
// }

// XNetCleanup - Network shutdown
// PPC_FUNC void stub_XNetCleanup(PPCContext& ctx, uint32_t addr) {
//     printf("[VOOT] STUB: XNetCleanup()\n");
//     ctx.r3.u64 = 0;
// }

// WSAStartup - Winsock initialization (Xbox 360 variant)
// PPC_FUNC void stub_WSAStartup(PPCContext& ctx, uint32_t addr) {
//     printf("[VOOT] STUB: WSAStartup() -> 0\n");
//     ctx.r3.u64 = 0;
// }

// ============================================================================
// XAM UI Stubs
// ============================================================================
// Xbox 360 dashboard/guide UI functions. These are called for things like
// sign-in prompts, marketplace, achievements display, etc.

// XamShowSigninUI
// PPC_FUNC void stub_XamShowSigninUI(PPCContext& ctx, uint32_t addr) {
//     printf("[VOOT] STUB: XamShowSigninUI() -> skipped\n");
//     ctx.r3.u64 = 0;
// }

// XamShowMessageBoxUI
// PPC_FUNC void stub_XamShowMessageBoxUI(PPCContext& ctx, uint32_t addr) {
//     printf("[VOOT] STUB: XamShowMessageBoxUI() -> OK button (0)\n");
//     ctx.r3.u64 = 0;
// }

// ============================================================================
// Content / DLC Stubs
// ============================================================================
// Virtual On OT may check for DLC or content licenses.

// XamContentGetLicenseMask - Content license check
// Returns full license mask to bypass any trial/demo restrictions
// PPC_FUNC void stub_XamContentGetLicenseMask(PPCContext& ctx, uint32_t addr) {
//     printf("[VOOT] STUB: XamContentGetLicenseMask() -> 0xFFFFFFFF (full license)\n");
//     // r4 = pointer to license mask output
//     // uint32_t* mask_ptr = (uint32_t*)rex::kernel::resolveGuestPtr(ctx.r4.u32);
//     // if (mask_ptr) *mask_ptr = 0xFFFFFFFF;
//     ctx.r3.u64 = 0;  // Return SUCCESS
// }

// ============================================================================
// Achievement Stubs
// ============================================================================

// XamUserWriteAchievements
// PPC_FUNC void stub_XamUserWriteAchievements(PPCContext& ctx, uint32_t addr) {
//     printf("[VOOT] STUB: XamUserWriteAchievements()\n");
//     ctx.r3.u64 = 0;
// }

// ============================================================================
// Storage / Save Data Stubs
// ============================================================================
// Save data will need real implementation eventually, but stub for now.

// XamContentCreateEnumerator
// PPC_FUNC void stub_XamContentCreateEnumerator(PPCContext& ctx, uint32_t addr) {
//     printf("[VOOT] STUB: XamContentCreateEnumerator() -> ERROR_NO_MORE_FILES\n");
//     ctx.r3.u64 = 0x80070012;  // ERROR_NO_MORE_FILES
// }

// ============================================================================
// Game-Specific Overrides
// ============================================================================
// These override specific game functions to modify behavior.
// Addresses will be filled in as they are identified during debugging.

// Example: Force all mechs unlocked
// PPC_FUNC void sub_82XXXXXX(PPCContext& ctx, uint32_t addr) {
//     // Force unlock bits before calling original
//     // auto* save = rex::kernel::resolveGuestPtr<VootSaveData>(ctx.r3.u32);
//     // save->unlock_flags |= 0xFFFF;
//     // Call original function
//     // sub_82XXXXXX_original(ctx, addr);
// }

// ============================================================================
// Stub Registration
// ============================================================================
// This will be called during init to register stubs for known import addresses.

void voot_register_stubs() {
    printf("[VOOT] Registering API stubs...\n");

    // These will be populated once we have the import address table from codegen:
    // rex::kernel::registerStub(0x82XXXXXX, stub_XNetStartup, "XNetStartup");
    // rex::kernel::registerStub(0x82XXXXXX, stub_XNetCleanup, "XNetCleanup");
    // rex::kernel::registerStub(0x82XXXXXX, stub_WSAStartup, "WSAStartup");
    // ... etc

    printf("[VOOT] Stubs registered (awaiting import table from codegen)\n");
}
