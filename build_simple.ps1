# Simple build script for AeroHack 2025 Rubik's Cube Solver
Write-Host "Building AeroHack 2025 Rubik's Cube Solver..." -ForegroundColor Green

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Configure and build with CMake
Write-Host "Configuring with CMake..." -ForegroundColor Yellow
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release

Write-Host "Building project..." -ForegroundColor Yellow
cmake --build . --config Release

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "Run: .\Release\rubiks_solver.exe --demo" -ForegroundColor Cyan
} else {
    Write-Host "Build failed!" -ForegroundColor Red
}

cd ..
