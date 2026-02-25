// Virtual On: Oratorio Tangram - Menu System Implementation

#include "menu.h"
#include "settings.h"

#include <cstdio>

void VootMenuSystem::init() {
    printf("[VOOT] Menu system initialized\n");
    // TODO: Create Win32 menu bar
    // TODO: Register ImGui dialogs with ReXGlue UI system
}

void VootMenuSystem::shutdown() {
    printf("[VOOT] Menu system shutdown\n");
}

void VootMenuSystem::update() {
    // TODO: ImGui dialog rendering
    // if (m_graphicsDialogOpen) { ... }
    // if (m_controlsDialogOpen) { ... }
}

void VootMenuSystem::showGraphicsConfig() {
    m_graphicsDialogOpen = true;
    printf("[VOOT] Opening graphics config\n");
}

void VootMenuSystem::showControlsConfig() {
    m_controlsDialogOpen = true;
    printf("[VOOT] Opening controls config (twin stick mapping!)\n");
}

void VootMenuSystem::showGameConfig() {
    m_gameDialogOpen = true;
    printf("[VOOT] Opening game config\n");
}

void VootMenuSystem::showDebugConfig() {
    m_debugDialogOpen = true;
    printf("[VOOT] Opening debug config\n");
}

void VootMenuSystem::showAbout() {
    m_aboutDialogOpen = true;
    printf("[VOOT] ========================================\n");
    printf("[VOOT]   Virtual On: Oratorio Tangram\n");
    printf("[VOOT]   Native PC Static Recompilation\n");
    printf("[VOOT]   Get in the Virtuaroid!\n");
    printf("[VOOT] ========================================\n");
}

void VootMenuSystem::saveState(int slot) {
    printf("[VOOT] Saving state to slot %d...\n", slot);
    // TODO: rex::runtime::saveState(slot);
}

void VootMenuSystem::loadState(int slot) {
    printf("[VOOT] Loading state from slot %d...\n", slot);
    // TODO: rex::runtime::loadState(slot);
}
