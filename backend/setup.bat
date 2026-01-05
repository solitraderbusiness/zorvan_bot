@echo off
echo ========================================
echo Zorvan Bot - Windows Setup Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)
python --version
echo [OK] Python found
echo.

echo Verifying all files exist...
python verify_files.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Setup cannot continue due to missing files.
    pause
    exit /b 1
)
echo.

echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

echo Creating .env file...
if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo [OK] .env file created
) else (
    echo [OK] .env file already exists
)
echo.

echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Install packages: pip install -r requirements.txt
echo 3. Run backend: uvicorn app.main:app --reload
echo.
echo Note: Package installation may take 5-10 minutes.
echo.
pause
