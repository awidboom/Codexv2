@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem Run from repo root even if launched elsewhere
pushd "%~dp0" >nul

set "PYEXE=python"
set "PYPARAMS="
where python >nul 2>nul
if errorlevel 1 (
  set "PYEXE=py"
  set "PYPARAMS=-3"
)

set "NO_REFRESH=0"
set "FORCE=0"
set "ARGS="

for %%A in (%*) do (
  if /I "%%~A"=="--no-refresh" set "NO_REFRESH=1"
  if /I "%%~A"=="--force" set "FORCE=1"
  if /I "%%~A"=="--force" (
    rem do not forward to Python
  ) else (
    set "ARGS=!ARGS! %%~A"
  )
)

if not exist "outputs" mkdir "outputs" >nul 2>nul

if %NO_REFRESH%==0 if %FORCE%==0 (
  tasklist /FI "IMAGENAME eq EXCEL.EXE" 2>nul | find /I "EXCEL.EXE" >nul
  if not errorlevel 1 (
    echo [update_dashboard] Excel is currently running.
    echo [update_dashboard] Close Excel first, or rerun with --no-refresh, or ^(at your own risk^) --force.
    popd >nul
    exit /b 2
  )
)

echo [update_dashboard] %DATE% %TIME%
echo [update_dashboard] %PYEXE% %PYPARAMS% scripts\dashboard.py%ARGS%
%PYEXE% %PYPARAMS% scripts\dashboard.py%ARGS%
set "RC=%ERRORLEVEL%"
echo [update_dashboard] Exit code: %RC%

popd >nul
exit /b %RC%
