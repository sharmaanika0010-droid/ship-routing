@echo off
title 🚢 Optimal Ship Routing System
color 1F
cls

echo.
echo  ============================================
echo    OPTIMAL SHIP ROUTING SYSTEM - v1.0
echo    Indian Ocean Region
echo  ============================================
echo.

cd /d "%~dp0"

echo  [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found!
    echo  Please install Python from python.org
    pause
    exit
)
echo  Python found!

echo.
echo  [2/3] Installing required libraries...
pip install -r requirements.txt -q
echo  Libraries ready!

echo.
echo  [3/3] Starting Ship Routing System...
echo.
echo  ============================================
echo.

python src/main.py

echo.
echo  ============================================
echo  Opening route map in browser...
echo  ============================================
echo.

if exist route_map.html (
    start route_map.html
    echo  Map opened in browser!
) else (
    echo  Map file not found - run the program first
)

echo.
echo  Press any key to exit...
pause >nul