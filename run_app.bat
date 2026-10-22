@echo off
REM Installs Streamlit (if needed) and opens the Vanguard A/B test app.
cd /d "%~dp0"

set "PY="
where py >nul 2>nul && set "PY=py"
if not defined PY if exist "%USERPROFILE%\anaconda3\python.exe" set "PY=%USERPROFILE%\anaconda3\python.exe"
if not defined PY where python >nul 2>nul && set "PY=python"

if not defined PY (
    echo Could not find Python on this computer.
    pause
    exit /b 1
)

echo Using Python: %PY%
"%PY%" -c "import streamlit" 2>nul || (
    echo Installing Streamlit, this can take a minute...
    "%PY%" -m pip install streamlit
)

echo Starting the app at http://localhost:8501  (close this window to stop it)
"%PY%" -m streamlit run streamlit_app.py
pause
