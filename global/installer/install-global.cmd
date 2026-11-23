@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo OpenClone Global Installer (Windows)
echo ===================================================

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%..\.."
for %%i in ("%REPO_ROOT%") do set "REPO_ROOT=%%~fi"

if defined OPENCLONE_HOME (
    set "TARGET_HOME=%OPENCLONE_HOME%"
) else (
    set "TARGET_HOME=%USERPROFILE%\.openclone"
)

echo Repository Root: %REPO_ROOT%
echo Target Home:     %TARGET_HOME%

python "%REPO_ROOT%\src\openclone\installer\cli.py" install --scope user --home "%TARGET_HOME%" %*
if errorlevel 1 (
    echo [ERROR] Installation failed.
    exit /b 1
)

echo [SUCCESS] OpenClone Global Installation completed.
exit /b 0
