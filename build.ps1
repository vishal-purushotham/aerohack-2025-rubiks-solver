# AeroHack 2025 Rubik's Cube Solver Build Script
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  AeroHack 2025 Rubik's Cube Solver  " -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (!(Test-Path "src\main.cpp")) {
    Write-Error "Please run this script from the project root directory"
    exit 1
}

# Step 1: Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Green
try {
    & python --version
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python found" -ForegroundColor Green
        & pip install -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Python dependencies installed" -ForegroundColor Green
        } else {
            Write-Warning "Python dependencies installation failed, but continuing..."
        }
    } else {
        Write-Warning "Python not found. AR features will not be available."
    }
} catch {
    Write-Warning "Python/pip not found. AR features will not be available."
}

Write-Host ""

# Step 2: Check for CMake
Write-Host "🔧 Checking build tools..." -ForegroundColor Green
try {
    & cmake --version | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ CMake found" -ForegroundColor Green
    } else {
        Write-Error "CMake not found. Please install CMake and add it to PATH."
        exit 1
    }
} catch {
    Write-Error "CMake not found. Please install CMake and add it to PATH."
    exit 1
}

# Step 3: Create build directory
Write-Host "📁 Preparing build directory..." -ForegroundColor Green
if (!(Test-Path "build")) {
    New-Item -ItemType Directory -Path "build" | Out-Null
    Write-Host "✓ Build directory created" -ForegroundColor Green
} else {
    Write-Host "✓ Build directory exists" -ForegroundColor Green
}

# Step 4: Configure with CMake
Write-Host "⚙️  Configuring with CMake..." -ForegroundColor Green
cd build
try {
    & cmake .. -DCMAKE_BUILD_TYPE=Release
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ CMake configuration successful" -ForegroundColor Green
    } else {
        Write-Error "CMake configuration failed"
        exit 1
    }
} catch {
    Write-Error "CMake configuration failed"
    exit 1
}

# Step 5: Build the project
Write-Host "🔨 Building project..." -ForegroundColor Green
try {
    & cmake --build . --config Release
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Build successful!" -ForegroundColor Green
    } else {
        Write-Error "Build failed"
        exit 1
    }
} catch {
    Write-Error "Build failed"
    exit 1
}

# Step 6: Success message
Write-Host ""
Write-Host "🎉 Build Complete!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green
Write-Host ""
Write-Host "Executables created:" -ForegroundColor Yellow
Write-Host "  .\Release\rubiks_solver.exe  - Main solver" -ForegroundColor White
Write-Host "  .\Release\test_cube.exe      - Cube tests" -ForegroundColor White
Write-Host "  .\Release\test_solver.exe    - Solver tests" -ForegroundColor White
Write-Host ""
Write-Host "Quick start:" -ForegroundColor Yellow
Write-Host "  .\Release\rubiks_solver.exe --demo" -ForegroundColor White
Write-Host "  .\Release\rubiks_solver.exe --python" -ForegroundColor White
Write-Host "  .\Release\rubiks_solver.exe 'R U R U'" -ForegroundColor White
Write-Host ""

# Return to project root
cd ..
