cmake_minimum_required(VERSION 3.28)

# Platform Support Floor Law: Apple Silicon only (arm64), macOS 14.0+.
# Cache entries set before project() so the floor governs every subdirectory and
# a standalone build enforces the same floor. A user -D override is preserved.
if(APPLE)
    set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Platform Support Floor Law: Apple Silicon only (arm64)")
    set(CMAKE_OSX_DEPLOYMENT_TARGET "14.0" CACHE STRING "Platform Support Floor Law: macOS 14.0+")
endif()

project(vexgraph C OBJC)

enable_testing()

# Platform Support Floor Law: Windows 10 floor.
if(WIN32)
    add_compile_definitions(_WIN32_WINNT=0x0A00 WINVER=0x0A00)
endif()

set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_OBJC_STANDARD 23)
set(CMAKE_OBJC_STANDARD_REQUIRED ON)

# Release: dead-code stripping so unused symbols (e.g. symmetric
# getters/setters nothing calls) cost zero bytes in shipped artifacts.
if(APPLE)
    add_compile_options($<$<CONFIG:Release>:-ffunction-sections> $<$<CONFIG:Release>:-fdata-sections>)
    add_link_options($<$<CONFIG:Release>:-Wl,-dead_strip>)
elseif(UNIX)
    add_compile_options($<$<CONFIG:Release>:-ffunction-sections> $<$<CONFIG:Release>:-fdata-sections>)
    add_link_options($<$<CONFIG:Release>:-Wl,--gc-sections>)
endif()

find_package(Vulkan QUIET)
if(NOT Vulkan_FOUND AND APPLE)
    execute_process(COMMAND brew --prefix OUTPUT_VARIABLE BREW_PREFIX OUTPUT_STRIP_TRAILING_WHITESPACE ERROR_QUIET)
    if(BREW_PREFIX AND EXISTS "${BREW_PREFIX}/include/vulkan/vulkan.h")
        set(Vulkan_INCLUDE_DIRS "${BREW_PREFIX}/include")
        set(Vulkan_FOUND TRUE)
    endif()
endif()

# Global include paths for the layers currently IN the renovation build.
# graphvex owns the language; vexspoke is its only upstream (R2).
include_directories(
        ${CMAKE_CURRENT_SOURCE_DIR}/ecosystem/vexspoke/src
        ${CMAKE_CURRENT_SOURCE_DIR}/ecosystem/graphvex/src
)

if(Vulkan_FOUND)
    include_directories(${Vulkan_INCLUDE_DIRS})
endif()

# Unified SPV shader staging for the runtime loader (graphvex shaders).
set(UNIFIED_SPV_DIR "${CMAKE_BINARY_DIR}/spv")
file(MAKE_DIRECTORY "${UNIFIED_SPV_DIR}")
file(GLOB_RECURSE ALL_SPV_FILES
    "${CMAKE_CURRENT_SOURCE_DIR}/ecosystem/graphvex/shader/spv/*.spv"
)
foreach(SPV_PATH ${ALL_SPV_FILES})
    get_filename_component(SPV_NAME "${SPV_PATH}" NAME)
    configure_file("${SPV_PATH}" "${UNIFIED_SPV_DIR}/${SPV_NAME}" COPYONLY)
endforeach()

# ============================================================================
# RENOVATION WIRING — vexspoke + graphvex + hotcwap + api-haven + darling.
#
# hotcwap (R1) and api-haven (R3) migrated off the old graphvex API and are
# re-wired above (verified: zero old includes; hotcwap keeps only the
# documented GfxLoop runner seat).
#
# darling-framework (R4) re-wires here: its layout record is fused into
# graphvex (darling/component.c deleted; component.h is a burn-down shim over
# lang/graphics_component.h) and the widget paint path now speaks the Graphics
# row (panel.h includes lang/image.h + lang/graphics.h; the retired
# vulkan/vk.h + image/image.h chain is gone). The build carries only the
# migrated sources — darling/CMakeLists.txt lists what has moved and parks the
# rest (frame, compositor, canvas, label/rich_label, the field/input family)
# until each returns in its own slice.
# ============================================================================
add_subdirectory(ecosystem/vexspoke)
add_subdirectory(ecosystem/graphvex)
# R1 + R3 — migrated off the old graphvex API (see the wiring note below).
add_subdirectory(ecosystem/hotcwap)
add_subdirectory(ecosystem/api-haven)
add_subdirectory(ecosystem/darling-framework)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/tests/CMakeLists.txt")
    enable_testing()
    add_subdirectory(tests)
endif()

# ----------------------------------------------------------------------------
# vk_test — the umbrella end-to-end probe (_main/test_suite.c), the R1 Kernel path.
#
# Kernel -> Application -> Window -> Frame. The only ObjC is image_load.m (the
# photo loader); the window lives in hotcwap (R1) and the Frame (R4) borrows it.
# ----------------------------------------------------------------------------
if(APPLE AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/_main/test_suite.c")
    add_executable(vk_test
        _main/test_suite.c
        _main/gallery.c
        _main/image_load.m
    )
    target_include_directories(vk_test PRIVATE
        _main
        ${CMAKE_CURRENT_SOURCE_DIR}/ecosystem/graphvex/src
        ${CMAKE_CURRENT_SOURCE_DIR}/ecosystem/darling-framework
    )
    target_compile_options(vk_test PRIVATE -Wall -Wextra -Werror)
    target_link_libraries(vk_test PRIVATE
        darling
        graphvex
        hotcwap
        pthread
        "-framework Cocoa"
        "-framework AppKit"
        "-framework QuartzCore"
        "-framework CoreGraphics"
    )
endif()

# ----------------------------------------------------------------------------
# scroll_probe — a CUSTOM Frame probe hosting the ScrollPanel scene
# (_main/scroll_probe.c). Its own Kernel -> Application -> Window -> Frame,
# separate from vk_test: the frame_demo scene owns darling Panels, so it lives
# in its own TU (the gallery.c precedent). Same shared scene as scroll_demo.
# ----------------------------------------------------------------------------
if(APPLE AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/_main/scroll_probe.c")
    add_executable(scroll_probe
        _main/scroll_probe.c
        _main/scroll_scene.c
    )
    target_include_directories(scroll_probe PRIVATE
        _main
        ${CMAKE_CURRENT_SOURCE_DIR}/ecosystem/graphvex/src
        ${CMAKE_CURRENT_SOURCE_DIR}/ecosystem/darling-framework
    )
    target_compile_options(scroll_probe PRIVATE -Wall -Wextra -Werror)
    target_link_libraries(scroll_probe PRIVATE
        darling
        graphvex
        hotcwap
        pthread
        "-framework Cocoa"
        "-framework AppKit"
        "-framework QuartzCore"
        "-framework CoreGraphics"
    )
endif()

# ----------------------------------------------------------------------------
# scroll_demo — the headless scroll probe (scripted frames -> BMP). Probes
# live in _main/ (the gallery.c precedent), never in a library repo. Same
# shared scene as the SCROLL_PROBE window above; no Cocoa, no window.
# ----------------------------------------------------------------------------
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/_main/scroll_demo.c")
    add_executable(scroll_demo
        _main/scroll_demo.c
        _main/scroll_scene.c
    )
    target_include_directories(scroll_demo PRIVATE _main)
    target_compile_options(scroll_demo PRIVATE -Wall -Wextra -Werror)
    target_link_libraries(scroll_demo PRIVATE darling graphvex vexspoke)
    add_executable(scroll_scene_tick_test
        tests/darling/scroll_scene_tick_test.c
        _main/scroll_scene.c
    )
    target_include_directories(scroll_scene_tick_test PRIVATE _main)
    target_compile_options(scroll_scene_tick_test PRIVATE -Wall -Wextra -Werror)
    target_link_libraries(scroll_scene_tick_test PRIVATE darling graphvex vexspoke)
    add_executable(scroll_scene_cull_test tests/darling/scroll_scene_cull_test.c)
    target_include_directories(scroll_scene_cull_test PRIVATE _main)
    target_compile_options(scroll_scene_cull_test PRIVATE -Wall -Wextra -Werror)
    target_link_libraries(scroll_scene_cull_test PRIVATE darling graphvex vexspoke)
    add_executable(scroll_scene_vulkan_test
        tests/darling/scroll_scene_vulkan_test.c
        _main/scroll_scene.c
    )
    target_include_directories(scroll_scene_vulkan_test PRIVATE _main)
    target_compile_options(scroll_scene_vulkan_test PRIVATE -Wall -Wextra -Werror)
    target_link_libraries(scroll_scene_vulkan_test PRIVATE darling graphvex vexspoke)
    add_executable(scroll_stress_bench
        tests/darling/scroll_stress_bench.c
        _main/scroll_scene.c
    )
    target_include_directories(scroll_stress_bench PRIVATE _main)
    target_compile_options(scroll_stress_bench PRIVATE -Wall -Wextra -Werror)
    target_link_libraries(scroll_stress_bench PRIVATE darling graphvex vexspoke)
    add_executable(scroll_million_panels_bench tests/darling/scroll_million_panels_bench.c)
    target_include_directories(scroll_million_panels_bench PRIVATE _main)
    target_compile_options(scroll_million_panels_bench PRIVATE -Wall -Wextra -Werror)
    target_link_libraries(scroll_million_panels_bench PRIVATE darling graphvex vexspoke)
endif()
