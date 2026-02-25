#pragma once

// Virtual On: Oratorio Tangram - Settings System
// Persists user configuration to voot_settings.toml.

#include <string>

struct VootSettings {
    // Graphics
    std::string render_path = "rov";   // "rov" or "rtv"
    int resolution_scale = 1;           // 1x, 2x, 3x, 4x internal resolution
    bool fullscreen = false;
    bool vsync = true;

    // Controls (Virtual On uses twin sticks!)
    int left_stick_controller = 0;      // SDL controller index for left stick
    int right_stick_controller = 0;     // SDL controller index for right stick
    bool single_controller_mode = true; // Map both sticks to one controller

    // Game
    bool force_unlock_all = false;      // Unlock all mechs/stages
    bool skip_intro = false;            // Skip intro movies

    // Debug
    bool show_fps = true;
    bool show_ppc_warnings = false;     // Show unimplemented PPC instruction warnings
    bool log_indirect_calls = false;    // Log all indirect function dispatch
    bool null_page_handler = true;      // Enable VEH null page handler

    // Load/save
    void load(const std::string& path = "voot_settings.toml");
    void save(const std::string& path = "voot_settings.toml") const;

    static VootSettings& instance();
};
