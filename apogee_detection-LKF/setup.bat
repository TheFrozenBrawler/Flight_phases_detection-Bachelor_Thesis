@echo off

:: Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo Python not found. Make sure Python is installed and added to your PATH.
    exit /b 1
)

:: Check if Python version is in required version or higher
set "python_major=3"
set "python_minor=11"
for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do for /f "tokens=1,2 delims=." %%b in ("%%a") do (
    if "%%b"=="%python_major%" if %%c GEQ %python_minor% goto :version_ok
    echo Python version %python_major%.%python_minor% or higher is required.
    exit /b 1
)
:version_ok

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Setup done! Use '.\run.bat' to run the program.