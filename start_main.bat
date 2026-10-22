@echo off
chcp 65001 >nul
title Multimodal AI Pipeline - Activity Logger

rem Project directory (relative to this script)
cd /d "%~dp0"

set LOG_FILE="%~dp0startup.log"

echo [%date% %time%] Starting main.py >> %LOG_FILE%

rem --- LM Studio: check API port 1234, start app if it is not running ---
netstat -ano | findstr ":1234" | findstr "LISTENING" >nul
if errorlevel 1 (
    if exist "%LOCALAPPDATA%\LM Studio\LM Studio.exe" (
        echo [%date% %time%] LM Studio API is down, launching LM Studio >> %LOG_FILE%
        start "" "%LOCALAPPDATA%\LM Studio\LM Studio.exe"
        ping -n 91 127.0.0.1 >nul
    ) else (
        echo [%date% %time%] WARNING: LM Studio not found, API may be unavailable >> %LOG_FILE%
    )
) else (
    echo [%date% %time%] LM Studio API is up >> %LOG_FILE%
)

rem --- Run the main script with the project virtual environment (auto-restart on crash) ---
:run_loop
"%~dp0.venv\Scripts\python.exe" "%~dp0main.py" >> %LOG_FILE% 2>&1
echo [%date% %time%] main.py exited, restarting in 30 seconds >> %LOG_FILE%
timeout /t 30 /nobreak >nul
goto run_loop
