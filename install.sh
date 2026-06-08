#!/usr/bin/env bash

set -e

echo "======================================"
echo "RVC RTX50 Installer"
echo "======================================"

# ================================
# Python 3.11 Check
# ================================

if command -v python3.11 >/dev/null 2>&1; then
    PYTHON=python3.11
else
    echo
    echo "[ERROR] Python 3.11 not found"
    echo
    echo "Ubuntu/Debian:"
    echo "  sudo apt install python3.11 python3.11-venv"
    echo
    echo "Arch:"
    echo "  sudo pacman -S python"
    echo
    exit 1
fi

echo "Using $($PYTHON --version)"

# ================================
# Create venv
# ================================

echo
echo "[1/6] Creating virtual environment..."

if [ ! -d "venv" ]; then
    $PYTHON -m venv venv
fi

source venv/bin/activate

# ================================
# Pip
# ================================

echo
echo "[2/6] Preparing pip..."

python -m ensurepip --upgrade || true

python -m pip install --upgrade setuptools wheel
python -m pip install "pip==24.0"

# ================================
# Torch
# ================================

echo
echo "[3/6] Installing PyTorch CUDA 12.8..."

pip install \
torch \
torchvision \
torchaudio \
--index-url https://download.pytorch.org/whl/cu128

# ================================
# Requirements
# ================================

echo
echo "[4/6] Installing requirements..."

pip install -r requirements.txt

# fairseq stack
pip install antlr4-python3-runtime==4.8
pip install omegaconf==2.0.5 --no-deps
pip install hydra-core==1.0.7 --no-deps
pip install fairseq==0.12.2 --no-deps

# ================================
# Assets
# ================================

echo
echo "[5/6] Preparing assets..."

mkdir -p assets/hubert
mkdir -p assets/rmvpe
mkdir -p assets/weights
mkdir -p logs

# ================================
# Downloader
# ================================

if command -v wget >/dev/null 2>&1; then
    DL="wget -O"
elif command -v curl >/dev/null 2>&1; then
    DL="curl -L -o"
else
    echo
    echo "[ERROR] wget or curl not found"
    exit 1
fi

# ================================
# Models
# ================================

echo
echo "[6/6] Downloading required models..."

if [ ! -f assets/hubert/hubert_base.pt ]; then
    $DL assets/hubert/hubert_base.pt \
    https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt
fi

if [ ! -f assets/rmvpe/rmvpe.pt ]; then
    $DL assets/rmvpe/rmvpe.pt \
    https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt
fi

echo
echo "======================================"
echo "INSTALLATION COMPLETE"
echo "Run:"
echo "./start.sh"
echo "======================================"
