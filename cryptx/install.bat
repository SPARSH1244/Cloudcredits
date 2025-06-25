@echo off
echo [🔧] Creating virtual environment...
python -m venv venv

echo [📦] Activating virtual environment...
call venv\Scripts\activate.bat

echo [⬇️] Installing required libraries...
pip install pyqt6 pycryptodome cryptography

echo [✅] Setup complete. You can now run the app using run.bat
pause
