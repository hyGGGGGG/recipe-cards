@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "PYTHON=%~dp0.venv\Scripts\python.exe"
set "COMMIT_MESSAGE=update recipes"

if not exist "%PYTHON%" (
    echo [ERROR] Virtual environment not found:
    echo %PYTHON%
    echo.
    echo Create it first with:
    echo py -V:3.14 -m venv .venv
    pause
    exit /b 1
)

"%PYTHON%" "%~dp0build.py"
if errorlevel 1 (
    echo.
    echo [ERROR] Build failed. Check the message above.
    pause
    exit /b 1
)

echo.
echo [OK] Menu page generated successfully.

where git >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Git was not found in PATH.
    pause
    exit /b 1
)

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] This directory is not a Git repository.
    pause
    exit /b 1
)

set "BRANCH="
for /f "delims=" %%B in ('git branch --show-current') do set "BRANCH=%%B"
if /i not "%BRANCH%"=="main" (
    echo.
    echo [ERROR] Automatic publishing is only allowed from the main branch.
    echo Current branch: %BRANCH%
    pause
    exit /b 1
)

git add -- recipes index.html build.bat
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to stage recipe files and generated page.
    pause
    exit /b 1
)

git diff --cached --quiet -- recipes index.html build.bat
if not errorlevel 1 (
    echo.
    echo [OK] No recipe changes to commit or push.
    pause
    exit /b 0
)

git commit -m "%COMMIT_MESSAGE%" -- recipes index.html build.bat
if errorlevel 1 (
    echo.
    echo [ERROR] Git commit failed. Nothing was pushed.
    pause
    exit /b 1
)

git push origin main
if errorlevel 1 (
    echo.
    echo [ERROR] Git push failed. The commit remains saved locally.
    pause
    exit /b 1
)

echo.
echo [OK] Changes committed and pushed to origin/main.
pause
