# AeroHack 2025 Rubik's Cube Solver

GPU-accelerated, AI-guided, blockchain-verifiable Rubik's Cube solver combining cutting-edge algorithms with modern technology stack.

## Features

- **Bitboard State Representation**: 64-bit optimized cube state encoding
- **Hybrid Heuristics**: Compressed Pattern Databases + Neural Network guidance
- **GPU Acceleration**: CUDA-powered IDA* search with parallel beam fallback
- **AR Scanner**: MediaPipe-based automatic cube state detection
- **Blockchain Verification**: Smart contract solution verification

## Requirements

- CUDA-capable GPU (Compute Capability ≥ 6.0)
- CMake ≥ 3.18
- C++17 compiler (gcc ≥ 8.0 or clang ≥ 7.0)
- Python ≥ 3.8
- LZ4 compression library

## Quick Start

```bash
# Build the project
mkdir build && cd build
cmake .. && cmake --build . --config Release

# Run solver
./Release/rubiks_solver "R U R' U' R U R' U'"
```

## Architecture

- **Core Engine**: Bitboard representation with move lookup tables
- **Pattern Databases**: LZ4-compressed heuristic databases (≤100MB)
- **Neural Heuristic**: 50k-parameter MLP trained via self-supervision
- **GPU Kernels**: Parallel IDA* with symmetry pruning
- **AR Interface**: Real-time cube scanning and visualization

## Performance Targets

- Median solve time: <200ms (CPU), <5ms (GPU)
- Solution length: ≤20 moves (median)
- Memory footprint: <120MB
- Accuracy: >99% optimal solutions

## License

MIT License - see LICENSE file for details.
