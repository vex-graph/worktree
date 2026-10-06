cmake_minimum_required(VERSION 3.24)

# IDE adapter only: b owns the ecosystem graph and runtime builds.
if(APPLE)
    set(CMAKE_OSX_ARCHITECTURES arm64 CACHE STRING "Native architecture")
    set(CMAKE_OSX_DEPLOYMENT_TARGET 14.0 CACHE STRING "Supported macOS floor")
endif()
project(vexgraph LANGUAGES C)
if(APPLE)
    enable_language(OBJC)
endif()
include(CTest)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
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
    "${CMAKE_SOURCE_DIR}/tools/b")
if(CMAKE_BUILD_TYPE MATCHES "^(Release|RelWithDebInfo|MinSizeRel)$")
    list(APPEND VEXGRAPH_B_COMMAND --release)
endif()
execute_process(COMMAND ${VEXGRAPH_B_COMMAND} ide
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
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
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    COMMENT "Building runtime with b (no apps or tests launched)"
    USES_TERMINAL VERBATIM)
file(GLOB_RECURSE source_inventory CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/ecosystem/repos/*.c" "${CMAKE_SOURCE_DIR}/ecosystem/repos/*.m"
    "${CMAKE_SOURCE_DIR}/tests/*_test.c")
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/tools/workspace.c" "${CMAKE_SOURCE_DIR}/tools/build_annotation.h"
    "${CMAKE_SOURCE_DIR}/tools/b")

# Real, excluded object targets give CLion a code model for production files.
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
        target_compile_definitions(${target} PRIVATE ${definitions})
        target_compile_options(${target} PRIVATE ${options}
            "$<$<COMPILE_LANGUAGE:OBJC>:-fobjc-arc>")
    endforeach()
endif()

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
        target_compile_definitions(${name} PRIVATE ${definitions})
        target_compile_options(${name} PRIVATE ${options} -UNDEBUG)
        target_link_libraries(${name} PRIVATE ${libraries})
        set_target_properties(${name} PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
        if(BUILD_TESTING)
            add_test(NAME ${name} COMMAND $<TARGET_FILE:${name}>)
            set_tests_properties(${name} PROPERTIES WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
                TIMEOUT 120 SKIP_RETURN_CODE 77 RUN_SERIAL TRUE LABELS "lab")
            if(NOT VEXGRAPH_ENABLE_WINDOW_TESTS AND
               (name IN_LIST window_tests OR sources MATCHES "/tests/(darling|graphvex)/"))
                set_tests_properties(${name} PROPERTIES DISABLED TRUE LABELS "lab;window-opt-in")
            endif()
        endif()
    endforeach()
endif()
message(STATUS "CLion: ${index_count} production indexing targets, ${test_count} native test targets from b")
message(STATUS "b remains build truth; window/GPU/UI CTest execution is opt-in")
