#pragma once

// Virtual On: Oratorio Tangram - Menu System
// Native Win32 menu bar + ImGui config dialogs for the recompiled game.

// #include <rex/ui/menu.h>
// #include <rex/ui/imgui_dialog.h>

class VootMenuSystem {
public:
    void init();
    void shutdown();
    void update();

    // Menu actions
    void showGraphicsConfig();
    void showControlsConfig();
    void showGameConfig();
    void showDebugConfig();
    void showAbout();

    // State save/load
    void saveState(int slot);
    void loadState(int slot);

private:
    bool m_graphicsDialogOpen = false;
    bool m_controlsDialogOpen = false;
    bool m_gameDialogOpen = false;
    bool m_debugDialogOpen = false;
    bool m_aboutDialogOpen = false;
};
