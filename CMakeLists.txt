cmake_minimum_required(VERSION 3.18)
project(RubiksSolver VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Try to find CUDA (optional)
find_package(CUDA QUIET)
if(CUDA_FOUND)
    enable_language(CUDA)
    add_definitions(-DUSE_CUDA)
endif()

# Try to find LZ4 (optional)
find_package(PkgConfig QUIET)
if(PKG_CONFIG_FOUND)
    pkg_check_modules(LZ4 liblz4)
    if(LZ4_FOUND)
        add_definitions(-DUSE_LZ4)
    endif()
endif()

# Include directories
include_directories(include)
include_directories(src)

# Core library
add_library(rubiks_core
    src/core/cube.cpp
    src/core/moves.cpp
    src/pdb/pattern_db.cpp
)

# GPU kernels (only if CUDA is available)
if(CUDA_FOUND)
    add_library(rubiks_gpu
        src/gpu/ida_kernel.cu
        src/gpu/beam_kernel.cu
    )
    set_property(TARGET rubiks_gpu PROPERTY CUDA_ARCHITECTURES 75)
endif()

# Main executable
add_executable(rubiks_solver
    src/main.cpp
)

# Link libraries
target_link_libraries(rubiks_solver rubiks_core)
if(CUDA_FOUND)
    target_link_libraries(rubiks_solver rubiks_gpu)
endif()
if(LZ4_FOUND)
    target_link_libraries(rubiks_solver ${LZ4_LIBRARIES})
endif()

# Tests
enable_testing()
add_executable(test_cube
    tests/test_cube.cpp
)
target_link_libraries(test_cube rubiks_core)

add_executable(test_solver
    tests/test_solver.cpp
)
target_link_libraries(test_solver rubiks_core)
