cmake_minimum_required(VERSION 3.24)

# IDE adapter only: b owns the ecosystem graph and runtime builds.
if(APPLE)
    set(CMAKE_OSX_ARCHITECTURES arm64 CACHE STRING "Native architecture")
    set(CMAKE_OSX_DEPLOYMENT_TARGET 14.0 CACHE STRING "Supported macOS floor")
endif()
project(vexgraph LANGUAGES C)
set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED YES)
set(CMAKE_C_EXTENSIONS YES)
if(APPLE)
    enable_language(OBJC)
    set(CMAKE_OBJC_STANDARD 23)
    set(CMAKE_OBJC_STANDARD_REQUIRED YES)
    set(CMAKE_OBJC_EXTENSIONS YES)
endif()
include(CTest)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(VEXGRAPH_SOURCE_ROOT "${CMAKE_CURRENT_SOURCE_DIR}")
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
if(CMAKE_CONFIGURATION_TYPES)
    message(FATAL_ERROR "Use a single-config generator for the b IDE adapter.")
endif()
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build configuration" FORCE)
endif()

# Keep IDE builds separate from the normal b build state.
set(VEXGRAPH_B_HOME "${CMAKE_BINARY_DIR}/b-state")
set(VEXGRAPH_B_COMMAND "${CMAKE_COMMAND}" -E env
    "B_HOME=${VEXGRAPH_B_HOME}" "PATH=$ENV{PATH}:/opt/homebrew/bin:$ENV{HOME}/.cargo/bin"
    "${VEXGRAPH_SOURCE_ROOT}/tools/b")
if(CMAKE_BUILD_TYPE MATCHES "^(Release|RelWithDebInfo|MinSizeRel)$")
    list(APPEND VEXGRAPH_B_COMMAND --release)
endif()
execute_process(COMMAND ${VEXGRAPH_B_COMMAND} ide
    WORKING_DIRECTORY "${VEXGRAPH_SOURCE_ROOT}"
    RESULT_VARIABLE graph_result OUTPUT_VARIABLE graph ERROR_VARIABLE graph_error)
if(NOT graph_result EQUAL 0)
    message(FATAL_ERROR "b could not export the IDE graph:\n${graph_error}")
endif()
file(WRITE "${CMAKE_BINARY_DIR}/b-test-graph.json" "${graph}")

function(graph_array output json)
    string(JSON count LENGTH "${json}" ${ARGN})
    set(items)
    if(count GREATER 0)
        math(EXPR last "${count} - 1")
        foreach(index RANGE 0 ${last})
            string(JSON item GET "${json}" ${ARGN} ${index})
            list(APPEND items "${item}")
        endforeach()
    endif()
    set(${output} "${items}" PARENT_SCOPE)
endfunction()

graph_array(byproducts "${graph}" byproducts)
add_custom_target(vexgraph_runtime
    COMMAND ${VEXGRAPH_B_COMMAND} build BYPRODUCTS ${byproducts}
    WORKING_DIRECTORY "${VEXGRAPH_SOURCE_ROOT}"
    COMMENT "Building runtime with b (no apps or tests launched)"
    USES_TERMINAL VERBATIM)
file(GLOB_RECURSE source_inventory CONFIGURE_DEPENDS
    "${VEXGRAPH_SOURCE_ROOT}/ecosystem/repos/*.c" "${VEXGRAPH_SOURCE_ROOT}/ecosystem/repos/*.m"
    "${VEXGRAPH_SOURCE_ROOT}/tests/*_test.c")
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS
    "${VEXGRAPH_SOURCE_ROOT}/tools/workspace.c" "${VEXGRAPH_SOURCE_ROOT}/tools/build_annotation.h"
    "${VEXGRAPH_SOURCE_ROOT}/tools/b")

# Real, excluded object targets give libraries, modules, apps and helper sources
# their owning code model. Application indexing never admits galleries to CTest.
# They do not replace b's runtime archives or participate in the default build.
string(JSON index_count LENGTH "${graph}" index)
if(index_count GREATER 0)
    math(EXPR last_index "${index_count} - 1")
    foreach(index RANGE 0 ${last_index})
        string(JSON record GET "${graph}" index ${index})
        string(JSON name GET "${record}" name)
        foreach(field sources includes definitions options)
            graph_array(${field} "${record}" ${field})
        endforeach()
        set(target "vexgraph_index_${name}")
        add_library(${target} OBJECT EXCLUDE_FROM_ALL ${sources})
        target_include_directories(${target} PRIVATE ${includes})
        if(VEXGRAPH_COMPILER_HEADERS)
            # Explicit options survive CMake's removal of implicit include dirs.
            target_compile_options(${target} PRIVATE -isystem "${VEXGRAPH_COMPILER_HEADERS}")
        endif()
        target_compile_definitions(${target} PRIVATE ${definitions})
        target_compile_options(${target} PRIVATE ${options}
            "$<$<COMPILE_LANGUAGE:OBJC>:-fobjc-arc>")
    endforeach()
endif()

# Harness's draft sources have no runtime b target yet. Reuse its indexing-only
# adapter instead of inventing a runtime target or duplicating its file list.
# Scope the local dependency path so other standalone adapters do not inherit it.
function(vexgraph_index_harness)
    set(VEXSPOKE_SOURCE_DIR "${VEXGRAPH_SOURCE_ROOT}/ecosystem/repos/vexspoke/src")
    add_subdirectory(ecosystem/repos/harness)
    if(VEXGRAPH_COMPILER_HEADERS)
        target_compile_options(harness_ide PRIVATE -isystem "${VEXGRAPH_COMPILER_HEADERS}")
    endif()
endfunction()
vexgraph_index_harness()

option(VEXGRAPH_ENABLE_WINDOW_TESTS "Enable window/GPU/UI CTest runs" OFF)
set(window_tests application_test bridge_seam_test present_surface_test traffic_light_test window_test)
string(JSON test_count LENGTH "${graph}" tests)
if(test_count GREATER 0)
    math(EXPR last_test "${test_count} - 1")
    foreach(index RANGE 0 ${last_test})
        string(JSON record GET "${graph}" tests ${index})
        string(JSON name GET "${record}" name)
        foreach(field sources includes definitions options libraries)
            graph_array(${field} "${record}" ${field})
        endforeach()
        add_executable(${name} ${sources})
        add_dependencies(${name} vexgraph_runtime)
        target_include_directories(${name} PRIVATE ${includes})
        if(VEXGRAPH_COMPILER_HEADERS)
            target_compile_options(${name} PRIVATE -isystem "${VEXGRAPH_COMPILER_HEADERS}")
        endif()
        target_compile_definitions(${name} PRIVATE ${definitions})
        target_compile_options(${name} PRIVATE ${options} -UNDEBUG)
        target_link_libraries(${name} PRIVATE ${libraries})
        set_target_properties(${name} PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
        if(BUILD_TESTING)
            add_test(NAME ${name} COMMAND $<TARGET_FILE:${name}>)
            set_tests_properties(${name} PROPERTIES WORKING_DIRECTORY "${VEXGRAPH_SOURCE_ROOT}"
                TIMEOUT 120 SKIP_RETURN_CODE 77 RUN_SERIAL TRUE LABELS "lab")
            if(NOT VEXGRAPH_ENABLE_WINDOW_TESTS AND
               (name IN_LIST window_tests OR sources MATCHES "/tests/(darling|graphvex)/"))
                set_tests_properties(${name} PROPERTIES DISABLED TRUE LABELS "lab;window-opt-in")
            endif()
        endif()
    endforeach()
endif()
message(STATUS "CLion: ${index_count} non-test indexing targets, ${test_count} native test targets from b")
message(STATUS "b remains build truth; window/GPU/UI CTest execution is opt-in")
