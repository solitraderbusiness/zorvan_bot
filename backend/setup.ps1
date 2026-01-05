# Windows Setup Script for Zorvan Bot Backend

Write-Host "Zorvan Bot - Windows Setup Script" -ForegroundColor Green
Write-Host "==================================`n" -ForegroundColor Green

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.11+ first." -ForegroundColor Red
    exit 1
}

# Verify we're in the backend directory
if (-not (Test-Path "app/main.py")) {
    Write-Host "✗ Please run this script from the backend directory" -ForegroundColor Red
    exit 1
}

# Run verification
Write-Host "`nVerifying all files exist..." -ForegroundColor Yellow
python verify_files.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nSetup cannot continue due to missing files." -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "`n✓ Virtual environment already exists" -ForegroundColor Green
}

# Create .env from .env.example if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "`nCreating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

Write-Host "`n==================================`n" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Activate virtual environment: venv\Scripts\activate"
Write-Host "2. Install packages: pip install -r requirements.txt"
Write-Host "3. Run backend: uvicorn app.main:app --reload"
Write-Host "`nNote: Package installation may take 5-10 minutes.`n" -ForegroundColor Cyan
