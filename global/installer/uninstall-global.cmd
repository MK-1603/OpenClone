@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo OpenClone Global Uninstaller (Windows)
echo ===================================================

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%..\.."
for %%i in ("%REPO_ROOT%") do set "REPO_ROOT=%%~fi"

if defined OPENCLONE_HOME (
    set "TARGET_HOME=%OPENCLONE_HOME%"
) else (
    set "TARGET_HOME=%USERPROFILE%\.openclone"
)

echo Target Home: %TARGET_HOME%

python "%REPO_ROOT%\src\openclone\installer\cli.py" uninstall --scope user --home "%TARGET_HOME%" %*
if errorlevel 1 (
    echo [ERROR] Uninstallation failed.
    exit /b 1
)

echo [SUCCESS] OpenClone Global Uninstallation completed.
exit /b 0
