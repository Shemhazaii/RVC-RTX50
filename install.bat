@echo off
setlocal EnableDelayedExpansion

title RVC Installer

echo ======================================
echo RVC RTX50 Installer
echo ======================================
echo.

where py >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found.
    echo Python 3.11 required.
    pause
    exit /b 1
)

REM ================================
REM Create venv
REM ================================

echo [1/7] Preparing Venv...

if not exist venv (
    py -3.11 -m venv venv
)

call venv\Scripts\activate.bat

REM ================================
REM Upgrade pip
REM ================================

echo.
echo [2/7] Upgrade pip...

python -m pip install pip==24.0
python -m pip install setuptools wheel

REM ================================
REM Install Torch
REM ================================

echo.
echo [3/7] Install PyTorch CUDA 12.8...

pip install ^
torch ^
torchvision ^
torchaudio ^
--index-url https://download.pytorch.org/whl/cu128

REM ================================
REM Install Requirements
REM ================================

echo.
echo [4/7] Install requirements...

pip install -r requirements.txt --no-binary pyworld

pip install antlr4-python3-runtime==4.8
pip install omegaconf==2.0.5 --no-deps
pip install hydra-core==1.0.7 --no-deps
pip install fairseq==0.12.2 --no-deps

REM ================================
REM Create Directories
REM ================================

echo.
echo [5/7] Preparing assets...

if not exist assets mkdir assets
if not exist assets\hubert mkdir assets\hubert
if not exist assets\rmvpe mkdir assets\rmvpe
if not exist assets\weights mkdir assets\weights
if not exist logs mkdir logs

REM ================================
REM Download Models
REM ================================

echo.
echo [6/7] Downloading required models...

if not exist assets\hubert\hubert_base.pt (
    echo Downloading HuBERT...
    powershell -Command ^
    "Invoke-WebRequest 'https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt' -OutFile 'assets\hubert\hubert_base.pt'"
)

if not exist assets\rmvpe\rmvpe.pt (
    echo Downloading RMVPE...
    powershell -Command ^
    "Invoke-WebRequest 'https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt' -OutFile 'assets\rmvpe\rmvpe.pt'"
)

REM ================================
REM Download FFMPEG
REM ================================

echo.
echo [7/7] Downloading ffmpeg...

if not exist tools mkdir tools

powershell -Command ^
 "Invoke-WebRequest https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -OutFile ffmpeg.zip"

powershell -Command ^
 "Expand-Archive ffmpeg.zip -DestinationPath ffmpeg_tmp"

for /r ffmpeg_tmp %%f in (ffmpeg.exe) do copy "%%f" tools\
for /r ffmpeg_tmp %%f in (ffprobe.exe) do copy "%%f" tools\

rmdir /s /q ffmpeg_tmp
del ffmpeg.zip

echo.
echo ======================================
echo INSTALLATION COMPLETE
echo Run start.bat
echo ======================================

pause