cmake_minimum_required(VERSION 3.18)
project(RubiksSolver VERSION 1.0.0 LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find packages
find_package(CUDA REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(LZ4 REQUIRED liblz4)

# Include directories
include_directories(include)
include_directories(src)

# Core library
add_library(rubiks_core
    src/core/cube.cpp
    src/core/moves.cpp
    src/pdb/pattern_db.cpp
)

# GPU kernels
add_library(rubiks_gpu
    src/gpu/ida_kernel.cu
    src/gpu/beam_kernel.cu
)

# Main executable
add_executable(rubiks_solver
    src/main.cpp
)

target_link_libraries(rubiks_solver 
    rubiks_core 
    rubiks_gpu
    ${LZ4_LIBRARIES}
)

# Tests
enable_testing()
add_executable(tests
    tests/test_cube.cpp
    tests/test_solver.cpp
)
target_link_libraries(tests rubiks_core)
