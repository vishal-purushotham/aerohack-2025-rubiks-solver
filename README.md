# AeroHack 2025 Professional Rubik's Cube Solver

**Professional-grade AR cube scanner + Hkociemba algorithm integration**

A production-ready Rubik's Cube solver combining professional QBR computer vision technology with Herbert Kociemba's world-class two-phase algorithm, enhanced with comprehensive configuration management and multi-language support.

## 🎯 Current Status: DAY 2 COMPLETE

### ✅ Day 1 Achievements (AR Integration)
- **Professional QBR Integration**: Complete webcam-based cube scanning system
- **Kociemba Algorithm**: Herbert Kociemba's optimal two-phase solver
- **Real-time AR Interface**: Live camera feed with cube state detection
- **Core Architecture**: Modular Python-based system with professional structure
- **Build System**: CMake + Python hybrid with comprehensive testing

### ✅ Day 2 Achievements (Professional Enhancement)
- **Configuration Management**: Centralized `config.json` with zero hardcoded values
- **Multi-language Support**: Complete i18n system (English, Spanish, French, German, Chinese)
- **Professional QBR**: Advanced computer vision with calibration and color detection
- **Error Handling**: Comprehensive validation and fallback systems
- **Code Quality**: Eliminated hardcoded values, professional logging, modular design

## 🔬 Technology Stack

### Core Solving Engine
- **Hkociemba Two-Phase Algorithm**: Herbert Kociemba's optimal solver
- **Professional QBR Scanner**: Computer vision-based cube state detection
- **Fallback Solvers**: Multi-tier solver architecture with graceful degradation

### Professional Features
- **Configuration-Driven**: All parameters externalized to `config.json`
- **Internationalization**: 5-language support with translation system
- **Advanced CV Pipeline**: Color calibration, contour detection, state validation
- **Performance Monitoring**: Real-time stats and solve time tracking

## 📋 Requirements

### Python Dependencies (Primary)
- Python ≥ 3.8
- OpenCV (cv2) for computer vision
- NumPy for array operations
- JSON for configuration management

### Optional C++ Build (Enhanced Performance)
- CUDA-capable GPU (Compute Capability ≥ 6.0)
- CMake ≥ 3.18
- C++17 compiler (gcc ≥ 8.0 or clang ≥ 7.0)
- LZ4 compression library

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/vishal-purushotham/aerohack-2025-rubiks-solver.git
cd aerohack-2025-rubiks-solver

# Install Python dependencies
pip install -r requirements.txt

# Build C++ components (optional - Python system works standalone)
mkdir build && cd build
cmake .. && cmake --build . --config Release
```

### Running the Professional AR Solver

```bash
# Navigate to Python source
cd src/python

# Professional AR scanning mode (default)
python ar_app.py

# Demo mode with test cubes
python ar_app.py --demo

# Manual solve mode
python ar_app.py --manual "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
```

### Professional AR Interface Usage

1. **Start Scanner**: Run `python ar_app.py`
2. **Color Calibration**: Press `C` to toggle calibration mode
3. **Scan Faces**: Follow on-screen instructions for each face
4. **Capture Stickers**: Press `SPACE` when contours are properly detected
5. **Professional Solving**: Algorithm automatically computes optimal solution
6. **Multi-language**: Interface supports EN/ES/FR/DE/ZH languages

## 🏗️ System Architecture

### Core Components

```
src/python/
├── ar_app.py              # Main AR application
├── kociemba_wrapper.py    # Professional Hkociemba integration
├── config_manager.py      # Configuration management system
├── config.json           # Centralized configuration
├── qbr/                  # Professional QBR computer vision
│   ├── video.py          # Webcam interface
│   ├── helpers.py        # Utility functions and i18n
│   └── constants.py      # Core QBR constants
├── twophase/             # Hkociemba two-phase algorithm
│   ├── solver.py         # Main solving interface
│   ├── cubie.py          # Cube state representation
│   └── misc.py           # Utility functions
└── translations/         # Multi-language support
    ├── en.json           # English
    ├── es.json           # Spanish
    ├── fr.json           # French
    ├── de.json           # German
    └── zh.json           # Chinese
```

## Architecture

## Architecture

### Professional QBR Computer Vision
- **Real-time Detection**: Webcam-based cube face scanning with live contour detection
- **Color Calibration**: Advanced color space analysis with calibration mode
- **State Validation**: Professional cube state verification using Hkociemba validation
- **Multi-camera Support**: Configurable camera selection and resolution

### Hkociemba Two-Phase Algorithm
- **Professional Implementation**: Herbert Kociemba's world-class optimal solver
- **Multi-tier Fallback**: Professional → Standard → Pattern-based solving
- **State Representation**: Cubie-level cube state with comprehensive validation
- **Optimal Solutions**: Guaranteed optimal or near-optimal move sequences

### Configuration Management
- **Centralized Config**: All parameters in `config.json` - zero hardcoded values
- **Runtime Flexibility**: Camera settings, solver parameters, UI customization
- **Professional Defaults**: Optimized parameters for production use
- **Easy Deployment**: Single config file for complete system customization

## 📊 Performance Characteristics

### Current Performance (Day 2)
- **Solving Speed**: Professional Hkociemba algorithm (optimal moves)
- **Detection Accuracy**: High-precision color calibration and contour detection  
- **Memory Footprint**: Lightweight Python implementation
- **Configuration**: Zero hardcoded values, fully configurable

### Professional Features
- **Multi-language Support**: 5 languages with complete translation system
- **Error Handling**: Comprehensive validation and graceful degradation
- **Professional Logging**: Detailed status and performance monitoring
- **Modular Design**: Clean separation of concerns, extensible architecture

## 🎮 Usage Examples

### Basic AR Scanning
```bash
cd src/python
python ar_app.py
# Follow on-screen instructions to scan your cube
```

### Demo Mode
```bash
python ar_app.py --demo
# Tests the system with known cube states
```

### Manual Solving
```bash
python ar_app.py --manual "DLRUUBFBRBLUFRLRLRLLLFFUUFRUBUUBDUUDLDRBDFRFDFFBBUDUL"
# Directly solve a cube string
```

### Configuration Customization
Edit `src/python/config.json`:
```json
{
  "solver": {
    "max_length": 25,
    "timeout_seconds": 10
  },
  "camera": {
    "camera_index": 0,
    "resolution": {"width": 640, "height": 480}
  }
}
```

## 🌍 Multi-language Support

The system includes complete internationalization:
- **English** (en): Default interface language
- **Spanish** (es): Interfaz en español
- **French** (fr): Interface en français  
- **German** (de): Deutsche Benutzeroberfläche
- **Chinese** (zh): 中文界面

Language files are in `src/python/translations/` and can be extended.

## 🔧 Development Status

### ✅ Completed (Day 1)
- Professional QBR integration
- Hkociemba algorithm wrapper
- Basic AR interface
- Core solving pipeline

### ✅ Completed (Day 2)  
- Configuration management system
- Complete hardcoded value elimination
- Multi-language support (5 languages)
- Professional error handling
- Code quality improvements

### 🚧 Future Enhancements
- GPU acceleration integration
- Performance optimization
- Advanced computer vision features
- Extended language support
- Cloud deployment capabilities

## License

MIT License - see LICENSE file for details.
