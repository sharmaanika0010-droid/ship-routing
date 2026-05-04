@echo off
title Optimal Ship Routing System
cls

echo.
echo  ================================================
echo       OPTIMAL SHIP ROUTING SYSTEM  v1.0
echo       Indian Ocean Region
echo  ================================================
echo.
echo  Setting up...
echo.

cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found. Install from python.org
    pause
    exit
)

pip install -r requirements.txt -q --disable-pip-version-check 2>nul
echo  All libraries ready.
echo.
echo  ================================================
echo.

python src/main.py

echo.
if exist route_map.html (
    echo  Opening map in browser...
    start route_map.html
) else (
    echo  Run the program first to generate the map.
)

echo.
pause