@echo off
echo 🚀 Starting Kiosk Scanner App
echo ================================

echo Checking Python installation...
python --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo 📱 Starting Kiosk Scanner API server...
echo Server will be available at: http://localhost:8000/api
echo.
echo To test: Open another terminal and run: python test_app.py
echo To stop: Press Ctrl+C
echo.

python app.py

pause
