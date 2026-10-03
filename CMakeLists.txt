cmake_minimum_required(VERSION 3.24)

# CLion adapter: b still owns the framework graph and builds its dependencies.
# CMake owns real test executables, giving CLion correct indexing + Run/Debug.
if(APPLE)
    set(CMAKE_OSX_ARCHITECTURES arm64 CACHE STRING "Native architecture")
    set(CMAKE_OSX_DEPLOYMENT_TARGET 14.0 CACHE STRING "Supported macOS floor")
endif()
project(vexgraph_tests LANGUAGES C)
include(CTest)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(CMAKE_CONFIGURATION_TYPES)
    message(FATAL_ERROR "Use a single-config generator (Ninja or Unix Makefiles) for this b adapter.")
endif()
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build configuration" FORCE)
endif()

# Independent state avoids simultaneous IDE/agent builds overwriting each other.
set(VEXGRAPH_B_HOME "${CMAKE_BINARY_DIR}/b-state")
set(VEXGRAPH_B_COMMAND "${CMAKE_COMMAND}" -E env "B_HOME=${VEXGRAPH_B_HOME}"
    "${CMAKE_SOURCE_DIR}/tools/b")
if(CMAKE_BUILD_TYPE STREQUAL "Release" OR CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo" OR
   CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
    list(APPEND VEXGRAPH_B_COMMAND --release)
endif()

execute_process(COMMAND ${VEXGRAPH_B_COMMAND} ide
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    RESULT_VARIABLE graph_result OUTPUT_VARIABLE graph ERROR_VARIABLE graph_error)
if(NOT graph_result EQUAL 0)
    message(FATAL_ERROR "b could not export the test graph:\n${graph_error}")
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
    COMMAND ${VEXGRAPH_B_COMMAND} build
    BYPRODUCTS ${byproducts}
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    COMMENT "Building framework dependencies with b (no tests or demos executed)"
    USES_TERMINAL VERBATIM)

# Re-export after target discovery changes, not just after CMakeLists changes.
file(GLOB_RECURSE test_inventory CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/tests/*_test.c")
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/tools/b.c")

option(VEXGRAPH_ENABLE_WINDOW_TESTS "Enable CTest tests that create real windows" OFF)
set(window_tests application_test bridge_seam_test present_surface_test
    traffic_light_test window_test)
string(JSON test_count LENGTH "${graph}" tests)
if(test_count GREATER 0)
    math(EXPR last_test "${test_count} - 1")
    foreach(index RANGE 0 ${last_test})
        string(JSON test_graph GET "${graph}" tests ${index})
        string(JSON name GET "${test_graph}" name)
        foreach(field sources includes definitions options libraries)
            graph_array(${field} "${test_graph}" ${field})
        endforeach()
        add_executable(${name} ${sources})
        add_dependencies(${name} vexgraph_runtime)
        target_include_directories(${name} PRIVATE ${includes})
        target_compile_definitions(${name} PRIVATE ${definitions})
        target_compile_options(${name} PRIVATE ${options})
        # Keep assertions active even with CMake's release-mode -DNDEBUG.
        target_compile_options(${name} PRIVATE -UNDEBUG)
        target_link_libraries(${name} PRIVATE ${libraries})
        set_target_properties(${name} PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
        if(BUILD_TESTING)
            add_test(NAME ${name} COMMAND $<TARGET_FILE:${name}>)
            set_tests_properties(${name} PROPERTIES
                WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}" TIMEOUT 120
                SKIP_RETURN_CODE 77 RUN_SERIAL TRUE LABELS "lab")
            if(NOT VEXGRAPH_ENABLE_WINDOW_TESTS AND
               (name IN_LIST window_tests OR sources MATCHES "/tests/(darling|graphvex)/"))
                # Still selectable Run/Debug targets: the user may opt in.
                set_tests_properties(${name} PROPERTIES DISABLED TRUE LABELS "lab;window-opt-in")
            endif()
        endif()
    endforeach()
endif()

message(STATUS "CLion: ${test_count} native test Run/Debug targets exported from b")
message(STATUS "Window/GPU/UI CTest runs are opt-in; visual approval belongs to the user")
