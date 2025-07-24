#!/bin/bash
# Build script for Rubik's Cube Solver

mkdir -p build
cd build
cmake ..
make -j$(nproc)
