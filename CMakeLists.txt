cmake_minimum_required(VERSION 3.24)

# IDE adapter only: b owns the vexgraph-ecosystem-gitrepo graph and runtime builds.
if(APPLE)
    set(CMAKE_OSX_ARCHITECTURES arm64 CACHE STRING "Native architecture")
    set(CMAKE_OSX_DEPLOYMENT_TARGET 14.0 CACHE STRING "Supported macOS floor")
endif()
project(vexgraph LANGUAGES C)
set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED YES)
set(CMAKE_C_EXTENSIONS YES)
if(APPLE AND CMAKE_C_COMPILER_ID MATCHES "Clang")
    # Shared code-model baseline, including b records without a CPU option.
    add_compile_options(-mcpu=apple-m1)
endif()
if(APPLE)
    enable_language(OBJC)
    set(CMAKE_OBJC_STANDARD 23)
    set(CMAKE_OBJC_STANDARD_REQUIRED YES)
    set(CMAKE_OBJC_EXTENSIONS YES)
endif()
include(CTest)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(VEXGRAPH_SOURCE_ROOT "${CMAKE_CURRENT_SOURCE_DIR}")
function(vexgraph_resolve_path output relative)
    if(relative MATCHES "^(host-behavior|drivers|interfaces)/(.*)$")
        set(resolved "suite/ecosystem/${CMAKE_MATCH_2}")
    elseif(relative MATCHES "^(interactables|superapp)/(.*)$")
        set(resolved "suite/projects/${CMAKE_MATCH_2}")
    elseif(relative MATCHES "^personal/(.*)$")
        set(resolved "suite/personal/${CMAKE_MATCH_1}")
    else()
        set(resolved "${relative}")
    endif()
    set(${output} "${VEXGRAPH_SOURCE_ROOT}/${resolved}" PARENT_SCOPE)
endfunction()
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

# One workspace entry owns recursive discovery. b-exported contexts remain
# untouched; supplemental excluded targets cover drafts and new source files.
# Each repository keeps its own include context, never one global header soup.
function(vexgraph_index_repository name relative template)
    vexgraph_resolve_path(source_root "${relative}")
    if(name STREQUAL "harness" AND VEXGRAPH_HARNESS_SOURCE_DIR)
        set(source_root "${VEXGRAPH_HARNESS_SOURCE_DIR}")
    endif()
    file(GLOB_RECURSE discovered CONFIGURE_DEPENDS
        "${source_root}/*.c" "${source_root}/*.h" "${source_root}/*.m")
    list(FILTER discovered EXCLUDE REGEX "/(attic|vendor|third_party|_old|cmake-build[^/]*|CMakeFiles)/")
    if(NOT APPLE)
        list(FILTER discovered EXCLUDE REGEX "\\.m$")
    endif()
    # Every remaining C/ObjC translation unit stays in the code model, including
    # other-host platform backends (window_linux, audio_stream_stub, ...). These
    # targets are EXCLUDE_FROM_ALL and never linked, so including them only adds
    # clangd diagnostics/inlay hints for files the current host does not build.
    set(unmodeled ${discovered})
    foreach(source IN LISTS VEXGRAPH_MODELED_SOURCES)
        list(REMOVE_ITEM unmodeled "${source}")
    endforeach()
    set(translation_units ${unmodeled})
    list(FILTER translation_units INCLUDE REGEX "\\.(c|m)$")
    if(NOT translation_units)
        return()
    endif()
    set(target "vexgraph_extra_${name}")
    add_library(${target} OBJECT EXCLUDE_FROM_ALL ${unmodeled})
    set_target_properties(${target} PROPERTIES LINKER_LANGUAGE C)
    if(TARGET "vexgraph_index_${template}")
        foreach(property INCLUDE_DIRECTORIES COMPILE_DEFINITIONS COMPILE_OPTIONS)
            get_target_property(value "vexgraph_index_${template}" ${property})
            if(value)
                set_property(TARGET ${target} PROPERTY ${property} "${value}")
            endif()
        endforeach()
    else()
        target_include_directories(${target} PRIVATE "${source_root}" ${ARGN})
        target_compile_options(${target} PRIVATE -std=gnu23 -Wall -Wextra -Werror)
        if(APPLE)
            target_compile_options(${target} PRIVATE -mcpu=apple-m1 "$<$<COMPILE_LANGUAGE:OBJC>:-fobjc-arc>")
        endif()
        if(VEXGRAPH_COMPILER_HEADERS)
            target_compile_options(${target} PRIVATE -isystem "${VEXGRAPH_COMPILER_HEADERS}")
        endif()
    endif()
endfunction()

set(VEXGRAPH_MODELED_SOURCES)
if(index_count GREATER 0)
    foreach(index RANGE 0 ${last_index})
        string(JSON record GET "${graph}" index ${index})
        graph_array(modeled "${record}" sources)
        list(APPEND VEXGRAPH_MODELED_SOURCES ${modeled})
    endforeach()
endif()
set(r2_cpu "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/vexspoke/src")
set(r2_storage "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/relational-engine/src")
vexgraph_index_repository(vexspoke host-behavior/vexspoke/src vexspoke)
vexgraph_index_repository(relational_engine host-behavior/relational-engine/src relational_engine)
vexgraph_index_repository(lifetime host-behavior/lifetime/src lifetime)
vexgraph_index_repository(hotcwap personal/hotcwap hotcwap)
vexgraph_index_repository(graphvex drivers/graphvex/src graphvex)
vexgraph_index_repository(api_haven personal/api-haven/src api_haven)
vexgraph_index_repository(determinant drivers/determinant/src determinant "${r2_cpu}" "${r2_storage}")
vexgraph_index_repository(darling interfaces/darling-framework/src darling)
vexgraph_index_repository(sesh interfaces/sesh/src sesh)
vexgraph_index_repository(darkbase-engine drivers/darkbase-engine/src darkbase-engine)
vexgraph_index_repository(impedance interactables/impedance/src impedance)
vexgraph_index_repository(samplerate drivers/samplerate/src "" "${r2_cpu}" "${r2_storage}")
set(VEXGRAPH_HARNESS_SOURCE_DIR "" CACHE PATH "Optional local Harness source tree for IDE indexing")
vexgraph_index_repository(harness interfaces/harness/src "" "${r2_cpu}")
vexgraph_index_repository(b personal/b "")
# Source-free blueprints produce no fake target. Future source files are found
# on CMake reload without introducing repository/directory CMake entries.
vexgraph_index_repository(language drivers/language "" "${r2_cpu}" "${r2_storage}")
vexgraph_index_repository(func personal/func/src "")
vexgraph_index_repository(primeagen personal/primeagen ""
    "${r2_cpu}" "${r2_storage}"
    "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/lifetime"
    "${VEXGRAPH_SOURCE_ROOT}/suite/personal/api-haven/src")
vexgraph_index_repository(tools tools "")
vexgraph_index_repository(notes _notes "")
foreach(application drawling)
    vexgraph_index_repository(${application} "interactables/${application}" ""
        "${r2_cpu}" "${r2_storage}")
endforeach()
vexgraph_index_repository(anti "superapp/anti" ""
    "${r2_cpu}" "${r2_storage}")
vexgraph_index_repository(semicolon "superapp/semicolon" ""
    "${VEXGRAPH_SOURCE_ROOT}/suite/projects/semicolon"
    "${VEXGRAPH_SOURCE_ROOT}/suite/projects/semicolon/src"
    "${VEXGRAPH_SOURCE_ROOT}/suite/projects/semicolon/icon"
    "${r2_cpu}" "${r2_storage}"
    "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/determinant/src"
    "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/language")

# Unregistered tests carry no b target, so no compile command reaches clangd.
# Mirror b's own per-subsystem include context so every test translation unit
# gets inlay hints without collapsing repositories into one header soup.
file(GLOB test_subsystems LIST_DIRECTORIES true "${VEXGRAPH_SOURCE_ROOT}/tests/*")
foreach(subsystem IN LISTS test_subsystems)
    if(NOT IS_DIRECTORY "${subsystem}")
        continue()
    endif()
    get_filename_component(test_name "${subsystem}" NAME)
    set(test_includes
        "${VEXGRAPH_SOURCE_ROOT}/tests"
        "${subsystem}"
        "${r2_cpu}" "${r2_storage}")
    if(test_name STREQUAL "lifetime")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/lifetime/src")
    elseif(test_name STREQUAL "hotcwap")
        list(APPEND test_includes
            "${VEXGRAPH_SOURCE_ROOT}/suite/personal/hotcwap"
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/lifetime/src")
    elseif(test_name STREQUAL "graphvex")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/graphvex/src")
    elseif(test_name STREQUAL "determinant")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/determinant/src")
    elseif(test_name STREQUAL "darling")
        list(APPEND test_includes
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/lifetime/src"
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/graphvex/src"
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/darling-framework/src")
    elseif(test_name STREQUAL "api-haven")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/personal/api-haven/src")
    elseif(test_name STREQUAL "sesh")
        list(APPEND test_includes
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/sesh/src"
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/sesh"
            "${VEXGRAPH_SOURCE_ROOT}/suite/personal/api-haven/src")
    elseif(test_name STREQUAL "darkbase-engine")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/darkbase-engine/src")
    elseif(test_name STREQUAL "harness")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/harness/src")
    elseif(test_name STREQUAL "language")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/language")
    elseif(test_name STREQUAL "samplerate")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/samplerate/src")
    elseif(test_name STREQUAL "primeagen")
        list(APPEND test_includes
            "${VEXGRAPH_SOURCE_ROOT}/suite/personal/primeagen"
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/lifetime/src"
            "${VEXGRAPH_SOURCE_ROOT}/suite/personal/api-haven/src"
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/harness/src")
    elseif(test_name STREQUAL "b")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/personal/b")
    elseif(test_name STREQUAL "func")
        list(APPEND test_includes "${VEXGRAPH_SOURCE_ROOT}/suite/personal/func/src")
    elseif(test_name STREQUAL "semicolon")
        list(APPEND test_includes
            "${VEXGRAPH_SOURCE_ROOT}/suite/projects/semicolon"
            "${VEXGRAPH_SOURCE_ROOT}/suite/projects/semicolon/src"
            "${VEXGRAPH_SOURCE_ROOT}/suite/projects/semicolon/icon"
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/determinant/src"
            "${VEXGRAPH_SOURCE_ROOT}/suite/ecosystem/language")
    endif()
    vexgraph_index_repository("tests_${test_name}" "tests/${test_name}" "" ${test_includes})
endforeach()

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
if(BUILD_TESTING)
    add_test(NAME opencode_preferences_test
        COMMAND "${VEXGRAPH_SOURCE_ROOT}/tools/b" test opencode_preferences)
    add_test(NAME checklist_runner_test
        COMMAND "${VEXGRAPH_SOURCE_ROOT}/tools/b" test checklist_runner)
    set_tests_properties(opencode_preferences_test checklist_runner_test PROPERTIES
        WORKING_DIRECTORY "${VEXGRAPH_SOURCE_ROOT}" TIMEOUT 120 RUN_SERIAL TRUE LABELS "lab;tooling")
endif()
message(STATUS "CLion: ${index_count} non-test indexing targets, ${test_count} native test targets from b")
message(STATUS "b remains build truth; window/GPU/UI CTest execution is opt-in")
