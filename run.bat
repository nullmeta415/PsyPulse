@echo off
echo ========================================
echo    Running PsyPulse
echo ========================================

REM Step 1: Check if virtual environment exists
IF NOT EXIST ".venv" (
    echo Virtual environment not found. Running setup_env.bat...
    CALL setup_env.bat %1
) ELSE (
    echo Virtual environment already exists. Skipping setup.
)

REM Step 2: Activate virtual environment
CALL .venv\Scripts\activate.bat

REM Step 3: Run the app
echo Starting PsyPulse...
python main.py

REM Step 4: Deactivate after run
deactivate
