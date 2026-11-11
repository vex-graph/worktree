cmake_minimum_required(VERSION 3.24)

# ============================================================================
# IDE ADAPTER ONLY — self-sufficient, no b, no b.assembly.json.
# ============================================================================
# b owns builds. This adapter owns everything the IDE needs that b does not:
# colours, symbol resolution, inlay hints, debug info, compile commands.
#
# This file lives at the repository root, beside `vex/` and `lib/`, so the CMake
# workspace IS the source tree it indexes. The generated build directory is
# deliberately outside that tree: .idea/cmake-build-debug, set by the CLion
# profile (GENERATION_DIR). Nothing below the repository root is written by
# CMake.
#
# Repositories, include roots and sources are derived from the filesystem,
# never declared here, so a new checkout under vex/ is indexed after a CMake
# reload with no other edit. The floor at lib/ (vex-c) is indexed alongside it.
# It creates no executable and no test target; every build and every run goes
# through b. The CLion run list lives in .idea/runConfigurations/ (git-ignored,
# like the rest of .idea/), not in CMake targets.
# ============================================================================

project(vexgraph-ecosystem LANGUAGES C)
set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED YES)
set(CMAKE_C_EXTENSIONS YES)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

if(APPLE)
    set(CMAKE_OSX_ARCHITECTURES arm64 CACHE STRING "Native architecture")
    set(CMAKE_OSX_DEPLOYMENT_TARGET 14.0 CACHE STRING "Supported macOS floor")
    enable_language(OBJC)
    set(CMAKE_OBJC_STANDARD 23)
    set(CMAKE_OBJC_STANDARD_REQUIRED YES)
    set(CMAKE_OBJC_EXTENSIONS YES)
endif()

# --- locate the tree --------------------------------------------------------
# The adapter sits at the repository root, so the root and the hub parent are
# unambiguous. VEXGRAPH_ROOT contains both `vex/` (the b tree) and `lib/`
# (vex-c); a copy placed elsewhere fails loudly instead of indexing a sibling.
get_filename_component(VEXGRAPH_ROOT "${CMAKE_CURRENT_SOURCE_DIR}" ABSOLUTE)
get_filename_component(VEXGRAPH_HUB "${VEXGRAPH_ROOT}/.." ABSOLUTE)
if(NOT IS_DIRECTORY "${VEXGRAPH_ROOT}/vex")
    message(FATAL_ERROR
        "vexgraph IDE adapter: ${VEXGRAPH_ROOT} has no `vex/` tree. Place "
        "CMakeLists.txt at the repository root, beside vex/ and lib/.")
endif()

message(STATUS "vexgraph IDE adapter: root ${VEXGRAPH_ROOT}")

# Some IDE clangd bundles omit their resource headers. Discover the selected
# compiler's headers instead of pinning an Xcode version or SDK installation.
set(VEXGRAPH_COMPILER_HEADERS "")
if(CMAKE_C_COMPILER_ID MATCHES "Clang")
    execute_process(COMMAND "${CMAKE_C_COMPILER}" -print-resource-dir
        OUTPUT_VARIABLE compiler_resource OUTPUT_STRIP_TRAILING_WHITESPACE
        RESULT_VARIABLE resource_result)
    if(resource_result EQUAL 0 AND EXISTS "${compiler_resource}/include/stddef.h")
        set(VEXGRAPH_COMPILER_HEADERS "${compiler_resource}/include")
    endif()
endif()

# --- include roots, derived from vex/ ---------------------------------------
# The flat library root (vex/) makes repository-prefixed includes resolve —
# #include "relational-engine/nio/mem.h" — while every repository's own root
# and src/ gives the subsystem-rooted form a home: #include "database/database.h".
# Rust FFI headers ride along through their rust/include dirs.
set(VEXGRAPH_INCLUDE_ROOTS
    "${VEXGRAPH_ROOT}"
    "${VEXGRAPH_ROOT}/vex"
    "${VEXGRAPH_ROOT}/vex/tests")

# vex-c (`lib`) sits at the repository root beside vex/. Adding it as an include
# root is what makes the bare `#include "vex.h"` door resolve from every tier.
get_filename_component(VEXGRAPH_VEXC_ROOT "${VEXGRAPH_ROOT}/lib" ABSOLUTE)
if(IS_DIRECTORY "${VEXGRAPH_VEXC_ROOT}")
    list(APPEND VEXGRAPH_INCLUDE_ROOTS "${VEXGRAPH_VEXC_ROOT}")
endif()
file(GLOB vex_entries LIST_DIRECTORIES true RELATIVE "${VEXGRAPH_ROOT}/vex"
    "${VEXGRAPH_ROOT}/vex/*")
foreach(entry IN LISTS vex_entries)
    if(NOT IS_DIRECTORY "${VEXGRAPH_ROOT}/vex/${entry}")
        continue()
    endif()
    list(APPEND VEXGRAPH_INCLUDE_ROOTS "${VEXGRAPH_ROOT}/vex/${entry}")
    if(IS_DIRECTORY "${VEXGRAPH_ROOT}/vex/${entry}/src")
        list(APPEND VEXGRAPH_INCLUDE_ROOTS "${VEXGRAPH_ROOT}/vex/${entry}/src")
    endif()
    if(IS_DIRECTORY "${VEXGRAPH_ROOT}/vex/${entry}/rust/include")
        list(APPEND VEXGRAPH_INCLUDE_ROOTS "${VEXGRAPH_ROOT}/vex/${entry}/rust/include")
    endif()
    # Some repositories root their subsystems one level down (darkbase's
    # engine/, b's adapters/). The union index prefers over-resolution to
    # missing symbols; b derives the precise per-unit roots at build time.
    file(GLOB sub_entries LIST_DIRECTORIES true RELATIVE "${VEXGRAPH_ROOT}/vex/${entry}"
        "${VEXGRAPH_ROOT}/vex/${entry}/*")
    foreach(sub IN LISTS sub_entries)
        if(IS_DIRECTORY "${VEXGRAPH_ROOT}/vex/${entry}/${sub}")
            list(APPEND VEXGRAPH_INCLUDE_ROOTS "${VEXGRAPH_ROOT}/vex/${entry}/${sub}")
        endif()
    endforeach()
endforeach()
list(REMOVE_DUPLICATES VEXGRAPH_INCLUDE_ROOTS)

# --- sources ----------------------------------------------------------------
# Every C/ObjC source under vex/, including the shared proof tree and the two
# tracked exceptions (annotation/, vex-test/). Headers need no object. The one
# Objective-C++ file (vexspoke's touchid demo) is deliberately not globbed:
# indexing it would enable OBJCXX, and some generators probe that compiler
# with the C standard flag, which it rejects — the IDE adapter stays C/ObjC
# only, and b's own build owns whatever that demo needs.
file(GLOB_RECURSE VEXGRAPH_SOURCES CONFIGURE_DEPENDS
    "${VEXGRAPH_ROOT}/vex/*.c"
    "${VEXGRAPH_ROOT}/vex/*.m")

# vex-c (`lib`) sits beside vex/ at the repository root. Its translation units
# belong in the code model too, or the IDE resolves `vex.h` but never indexes
# the implementation behind it.
if(IS_DIRECTORY "${VEXGRAPH_VEXC_ROOT}")
    file(GLOB_RECURSE VEXGRAPH_VEXC_SOURCES CONFIGURE_DEPENDS
        "${VEXGRAPH_VEXC_ROOT}/*.c")
    list(APPEND VEXGRAPH_SOURCES ${VEXGRAPH_VEXC_SOURCES})
endif()

list(FILTER VEXGRAPH_SOURCES EXCLUDE REGEX "/(\\.b|cmake-build[^/]*|CMakeFiles|\\.git)/")

# --- one excluded index library, no runnables --------------------------------
# One union target on purpose: the IDE code model wants the whole tree, not
# per-unit partitions. EXCLUDE_FROM_ALL keeps it out of every build.
add_library(vexgraph_index OBJECT EXCLUDE_FROM_ALL ${VEXGRAPH_SOURCES}
        vex/re/re.h
        vex/re/nio/nio.h
        lib/lang/lang.h
        vex/re/nio/arena.c)
if(EXISTS "${VEXGRAPH_VEXC_ROOT}/debug/main.c")
    target_sources(vexgraph_index PRIVATE "${VEXGRAPH_VEXC_ROOT}/debug/main.c")
endif()
set_target_properties(vexgraph_index PROPERTIES LINKER_LANGUAGE C)
target_include_directories(vexgraph_index PRIVATE ${VEXGRAPH_INCLUDE_ROOTS})
target_compile_options(vexgraph_index PRIVATE -std=gnu23 -Wall -Wextra)
if(VEXGRAPH_COMPILER_HEADERS)
    target_compile_options(vexgraph_index PRIVATE -isystem "${VEXGRAPH_COMPILER_HEADERS}")
endif()
if(APPLE)
    target_compile_options(vexgraph_index PRIVATE -mcpu=apple-m1
        "$<$<COMPILE_LANGUAGE:OBJC>:-fobjc-arc>")
endif()

list(LENGTH VEXGRAPH_INCLUDE_ROOTS vexgraph_root_count)
list(LENGTH VEXGRAPH_SOURCES vexgraph_source_count)
message(STATUS "vexgraph IDE adapter: ${vexgraph_source_count} sources, ${vexgraph_root_count} include roots, derived from vex/ and vex-c")
message(STATUS "b owns builds; reload CMake after adding files or repositories")
