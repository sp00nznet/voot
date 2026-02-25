// Virtual On: Oratorio Tangram - Headless Boot Test
// Console-only test harness for crash debugging without GPU.
// Runs the game's initialization sequence and reports where it dies.

#include <cstdio>
#include <cstdlib>

#include "voot_config.h"
// #include "voot_init.h"
// #include <rex/runtime/context.h>
// #include <rex/kernel/kernel.h>

#ifdef _WIN32
#include <windows.h>

static LONG CALLBACK CrashDiagnosticHandler(EXCEPTION_POINTERS* ep) {
    printf("\n[VOOT TEST] !!!! CRASH DETECTED !!!!\n");
    printf("[VOOT TEST] Exception code: 0x%08lX\n", ep->ExceptionRecord->ExceptionCode);
    printf("[VOOT TEST] Exception addr: 0x%016llX\n", (unsigned long long)ep->ExceptionRecord->ExceptionAddress);
    printf("[VOOT TEST] RIP: 0x%016llX\n", (unsigned long long)ep->ContextRecord->Rip);
    printf("[VOOT TEST] RAX: 0x%016llX\n", (unsigned long long)ep->ContextRecord->Rax);
    printf("[VOOT TEST] RCX: 0x%016llX\n", (unsigned long long)ep->ContextRecord->Rcx);
    printf("[VOOT TEST] RDX: 0x%016llX\n", (unsigned long long)ep->ContextRecord->Rdx);
    printf("[VOOT TEST] RBX: 0x%016llX\n", (unsigned long long)ep->ContextRecord->Rbx);
    printf("[VOOT TEST] RSP: 0x%016llX\n", (unsigned long long)ep->ContextRecord->Rsp);
    printf("[VOOT TEST] RBP: 0x%016llX\n", (unsigned long long)ep->ContextRecord->Rbp);
    printf("[VOOT TEST] RSI: 0x%016llX\n", (unsigned long long)ep->ContextRecord->Rsi);
    printf("[VOOT TEST] RDI: 0x%016llX\n", (unsigned long long)ep->ContextRecord->Rdi);
    printf("[VOOT TEST] R8:  0x%016llX\n", (unsigned long long)ep->ContextRecord->R8);
    printf("[VOOT TEST] R9:  0x%016llX\n", (unsigned long long)ep->ContextRecord->R9);
    printf("[VOOT TEST] R10: 0x%016llX\n", (unsigned long long)ep->ContextRecord->R10);
    printf("[VOOT TEST] R11: 0x%016llX\n", (unsigned long long)ep->ContextRecord->R11);
    printf("[VOOT TEST] R12: 0x%016llX\n", (unsigned long long)ep->ContextRecord->R12);
    printf("[VOOT TEST] R13: 0x%016llX\n", (unsigned long long)ep->ContextRecord->R13);
    printf("[VOOT TEST] R14: 0x%016llX\n", (unsigned long long)ep->ContextRecord->R14);
    printf("[VOOT TEST] R15: 0x%016llX\n", (unsigned long long)ep->ContextRecord->R15);

    if (ep->ExceptionRecord->ExceptionCode == EXCEPTION_ACCESS_VIOLATION) {
        ULONG_PTR access_type = ep->ExceptionRecord->ExceptionInformation[0];
        ULONG_PTR fault_addr = ep->ExceptionRecord->ExceptionInformation[1];
        const char* access_str = access_type == 0 ? "READ" :
                                 access_type == 1 ? "WRITE" : "DEP";
        printf("[VOOT TEST] Access violation: %s at 0x%016llX\n",
               access_str, (unsigned long long)fault_addr);
    }

    // Print instruction bytes at crash site
    printf("[VOOT TEST] Instruction bytes: ");
    BYTE* rip = (BYTE*)ep->ContextRecord->Rip;
    for (int i = 0; i < 16; i++) {
        printf("%02X ", rip[i]);
    }
    printf("\n");

    return EXCEPTION_CONTINUE_SEARCH;
}
#endif

int main(int argc, char* argv[]) {
    printf("========================================\n");
    printf("  VOOT - Headless Boot Test\n");
    printf("  No GPU - crash diagnostics only\n");
    printf("========================================\n\n");

#ifdef _WIN32
    AddVectoredExceptionHandler(1, CrashDiagnosticHandler);
#endif

    printf("[VOOT TEST] Image: 0x%08X - 0x%08X\n", VOOT_IMAGE_BASE, VOOT_IMAGE_BASE + VOOT_IMAGE_SIZE);

    // TODO: Initialize kernel (no GPU)
    // rex::kernel::init();

    // TODO: Register functions
    // voot_register_functions();

    // TODO: Run game init sequence
    // PPCContext ctx = {};
    // ctx.fpscr.csr = 0x1F80;  // Mask SSE exceptions
    // rex::runtime::callFunction(ctx, VOOT_IMAGE_BASE + VOOT_ENTRY_POINT);

    printf("[VOOT TEST] Boot test skeleton ready. Awaiting codegen.\n");

    return 0;
}
