@echo off
echo ===============================
echo  Setting up PsyPulse Environment
echo ===============================

REM Step 1: Check Python 3.12 is installed
py -3.12 --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python 3.12 not found. Please install Python 3.12.
    exit /b 1
)

REM Step 2: Create virtual environment if not exits
IF NOT EXIST .venv (
    echo Creating virutal environment (.venv)...
    py -3.12 -m venv .venv
) ELSE (
    echo Virtual environment already exits.
)

REM Step 3: Activate virtual environment
call .venv\Scripts\activate

REM Step 4: Upgrade pip
python -m pip install --upgrade pip

REM Step 5: Detect GPU (NVIDIA-SMI tool is available only if GPU drivers installed)
echo Checking for NVIDIA GPU...
nvidia-smi >nul 2>&1
IF ERRORLEVEL 1 (
    echo No NVIDIA GPU found. Installing CPU-only PyTorch...
    pip install torch torchvision torchaudio
) ELSE (
    echo NVIDIA GPU detected. Installing CUDA-enabled PyTorch (CUDA 12.6)...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
)

REM Step 6: Install other dependencies
echo Installing other dependencies...
pip install -r requirements.txt

REM Step 7: Verify torch + CUDA/CPU
echo Verifying installation...
python - <<EOF
import torch
print("Torch version: ", torch.__version__)
print("CUDA available: ", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU detected: ", torch.cuda.get_device_name(0))
else:
    print("Running on CPU only")
EOF

echo ===============================
echo  Setup Complete! Run with:
echo  .venv\Scripts\activate && python main.py
echo ===============================
pause