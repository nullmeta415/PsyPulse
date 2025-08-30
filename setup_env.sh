#!/bin/bash
echo "================================"
echo "   Setting up PsyPulse Environment"
echo "================================"

# --- Step 0: Parse arguments ---
INSTALL_MODE="auto"   # default
if [[ "$1" == "--cpu-only" ]]; then
    INSTALL_MODE="cpu"
elif [[ "$1" == "--gpu" ]]; then
    INSTALL_MODE="gpu"
fi

# Step 1: Check Python 3.12
if ! command -v python3.12 &> /dev/null
then
    echo "[ERROR] Python 3.12 not found. Please install Python 3.12."
    exit 1
fi

# Step 2: Create virtual environment if not exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)..."
    python3.12 -m venv .venv
else
    echo "Virtual environment already exists."
fi

# Step 3: Activate virtual environment
source .venv/bin/activate

# Step 4: Upgrade pip
python -m pip install --upgrade pip

# Step 5: Install PyTorch (CPU/GPU/auto)
if [[ "$INSTALL_MODE" == "cpu" ]]; then
    echo "Forcing CPU-only PyTorch install..."
    pip install torch torchvision torchaudio
elif [[ "$INSTALL_MODE" == "gpu" ]]; then
    echo "Forcing CUDA-enabled PyTorch install (CUDA 12.6)..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
else
    echo "Auto-detecting GPU..."
    if command -v nvidia-smi &> /dev/null; then
        echo "NVIDIA GPU detected. Installing CUDA-enabled PyTorch (CUDA 12.6)..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
    else
        echo "No NVIDIA GPU found. Installing CPU-only PyTorch..."
        pip install torch torchvision torchaudio
    fi
fi

# Step 6: Install other dependencies
echo "Installing other dependencies..."
pip install -r requirements.txt

# Step 7: Verify installation
echo "Verifying installation..."
python - <<EOF
import torch
print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU detected:", torch.cuda.get_device_name(0))
else:
    print("Running on CPU only")
EOF

echo "================================"
echo "   Setup Complete!"
echo "   Run with: source .venv/bin/activate && python main.py"
echo "================================"
