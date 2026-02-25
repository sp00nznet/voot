cmake_minimum_required(VERSION 3.25)
project(voot LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ReXGlue SDK - adjust path as needed
# set(REXGLUE_SDK_DIR "" CACHE PATH "Path to ReXGlue SDK")
# find_package(ReXGlue REQUIRED HINTS ${REXGLUE_SDK_DIR})

# Include generated source file list
include(${CMAKE_CURRENT_SOURCE_DIR}/../generated/sources.cmake)

# Project source files
set(VOOT_PROJECT_SOURCES
    src/main.cpp
    src/stubs.cpp
    src/menu.cpp
    src/settings.cpp
)

set(VOOT_PROJECT_HEADERS
    src/menu.h
    src/settings.h
)

# Main executable
add_executable(voot
    ${VOOT_PROJECT_SOURCES}
    ${VOOT_PROJECT_HEADERS}
    ${VOOT_GENERATED_SOURCES}
    ${VOOT_GENERATED_HEADERS}
)

target_include_directories(voot PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/../generated
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# ReXGlue SDK libraries
# target_link_libraries(voot PRIVATE
#     rex::core
#     rex::runtime
#     rex::kernel
#     rex::graphics
#     rex::ui
# )

# Compiler flags for recompiled PPC code
target_compile_options(voot PRIVATE
    # Required for PPC intrinsic translations
    $<$<CXX_COMPILER_ID:Clang>:-Wno-unused-variable>
    $<$<CXX_COMPILER_ID:Clang>:-Wno-unused-but-set-variable>
    $<$<CXX_COMPILER_ID:Clang>:-Wno-parentheses>
    # Performance - the generated code benefits from aggressive optimization
    $<$<CONFIG:Release>:-O2>
)

# Test executable (headless boot test)
add_executable(voot_test
    src/test_boot.cpp
    ${VOOT_GENERATED_SOURCES}
    ${VOOT_GENERATED_HEADERS}
)

target_include_directories(voot_test PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/../generated
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# target_link_libraries(voot_test PRIVATE
#     rex::core
#     rex::runtime
#     rex::kernel
# )

# Copy game data files next to executable if present
# add_custom_command(TARGET voot POST_BUILD
#     COMMAND ${CMAKE_COMMAND} -E copy_directory_if_different
#         ${CMAKE_CURRENT_SOURCE_DIR}/../gamedata
#         $<TARGET_FILE_DIR:voot>/gamedata
#     COMMENT "Copying game data..."
# )

message(STATUS "VOOT: Virtual On Oratorio Tangram Static Recompilation")
message(STATUS "  Generated sources: ${VOOT_GENERATED_SOURCES}")
message(STATUS "  Project sources:   ${VOOT_PROJECT_SOURCES}")
