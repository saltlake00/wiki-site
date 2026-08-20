@echo off
title sprite-gen web curation editor
setlocal

REM ============================================================
REM  sprite-gen curation web editor launcher
REM  Double-click to open the frame editor in your browser.
REM
REM  Usage:
REM    spritegen-curation.bat                  -> uses default run-dir
REM    spritegen-curation.bat <run-dir path>   -> uses your run-dir
REM ============================================================

REM ---- sprite-gen moved outside the wiki repo on 2026-08-20 ----
REM ---- adjust SPRITE_GEN below if it's installed elsewhere ----
set "SPRITE_GEN=C:\Users\KGA01\Documents\위키-참고자료\sprite-gen"
set "PY=%SPRITE_GEN%\.venv\Scripts\python.exe"
set "WIKI_BASE=G:\내 드라이브\wiki\projects\gamedev\pixel-sprite-workflow"

if not exist "%PY%" (
  echo [ERROR] python.exe not found:
  echo   %PY%
  echo   Edit SPRITE_GEN at the top of this file to point to your sprite-gen install.
  pause
  exit /b 1
)

REM ---- choose run-dir ----
set "RUN_DIR=%~1"
if "%RUN_DIR%"=="" set "RUN_DIR=%WIKI_BASE%\test-assets\varco-fantasy\run"

if not exist "%RUN_DIR%\sprite-request.json" (
  echo [ERROR] run-dir not ready:
  echo   %RUN_DIR%
  echo   Missing sprite-request.json.
  echo   Use: spritegen-curation.bat ^<path-to-run-dir^>
  pause
  exit /b 1
)

echo ============================================================
echo   sprite-gen web editor (curation)
echo   run-dir: %RUN_DIR%
echo   Browser will open. Press Ctrl+C in this window to stop.
echo ============================================================
echo.

cd /d "%RUN_DIR%"
"%PY%" -m sprite_gen.cli curation --run-dir . --lang ko

pause
