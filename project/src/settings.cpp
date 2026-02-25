// Virtual On: Oratorio Tangram - Settings Implementation
// Uses TOML for human-readable configuration persistence.

#include "settings.h"
#include <cstdio>
#include <fstream>

// TODO: #include <toml++/toml.h>

VootSettings& VootSettings::instance() {
    static VootSettings s;
    return s;
}

void VootSettings::load(const std::string& path) {
    printf("[VOOT] Loading settings from %s\n", path.c_str());

    // TODO: toml++ loading
    // try {
    //     auto config = toml::parse_file(path);
    //
    //     // Graphics
    //     render_path = config["graphics"]["render_path"].value_or("rov");
    //     resolution_scale = config["graphics"]["resolution_scale"].value_or(1);
    //     fullscreen = config["graphics"]["fullscreen"].value_or(false);
    //     vsync = config["graphics"]["vsync"].value_or(true);
    //
    //     // Controls
    //     left_stick_controller = config["controls"]["left_stick_controller"].value_or(0);
    //     right_stick_controller = config["controls"]["right_stick_controller"].value_or(0);
    //     single_controller_mode = config["controls"]["single_controller_mode"].value_or(true);
    //
    //     // Game
    //     force_unlock_all = config["game"]["force_unlock_all"].value_or(false);
    //     skip_intro = config["game"]["skip_intro"].value_or(false);
    //
    //     // Debug
    //     show_fps = config["debug"]["show_fps"].value_or(true);
    //     show_ppc_warnings = config["debug"]["show_ppc_warnings"].value_or(false);
    //     log_indirect_calls = config["debug"]["log_indirect_calls"].value_or(false);
    //     null_page_handler = config["debug"]["null_page_handler"].value_or(true);
    //
    //     printf("[VOOT] Settings loaded successfully\n");
    // } catch (const toml::parse_error& err) {
    //     printf("[VOOT] Could not load settings: %s\n", err.what());
    //     printf("[VOOT] Using defaults\n");
    // }
}

void VootSettings::save(const std::string& path) const {
    printf("[VOOT] Saving settings to %s\n", path.c_str());

    // TODO: toml++ saving
    // std::ofstream ofs(path);
    // if (!ofs) {
    //     printf("[VOOT] ERROR: Could not open %s for writing\n", path.c_str());
    //     return;
    // }
    //
    // ofs << "# Virtual On: Oratorio Tangram - Settings\n\n";
    //
    // ofs << "[graphics]\n";
    // ofs << "render_path = \"" << render_path << "\"\n";
    // ofs << "resolution_scale = " << resolution_scale << "\n";
    // ofs << "fullscreen = " << (fullscreen ? "true" : "false") << "\n";
    // ofs << "vsync = " << (vsync ? "true" : "false") << "\n\n";
    //
    // ofs << "[controls]\n";
    // ofs << "left_stick_controller = " << left_stick_controller << "\n";
    // ofs << "right_stick_controller = " << right_stick_controller << "\n";
    // ofs << "single_controller_mode = " << (single_controller_mode ? "true" : "false") << "\n\n";
    //
    // ofs << "[game]\n";
    // ofs << "force_unlock_all = " << (force_unlock_all ? "true" : "false") << "\n";
    // ofs << "skip_intro = " << (skip_intro ? "true" : "false") << "\n\n";
    //
    // ofs << "[debug]\n";
    // ofs << "show_fps = " << (show_fps ? "true" : "false") << "\n";
    // ofs << "show_ppc_warnings = " << (show_ppc_warnings ? "true" : "false") << "\n";
    // ofs << "log_indirect_calls = " << (log_indirect_calls ? "true" : "false") << "\n";
    // ofs << "null_page_handler = " << (null_page_handler ? "true" : "false") << "\n";
    //
    // printf("[VOOT] Settings saved\n");
}
