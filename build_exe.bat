@echo off
REM VoiceSnap - Build Launcher .exe for Windows
REM Utilise PyInstaller pour créer un executable standalone

echo ====================================
echo   VoiceSnap Launcher Builder
echo ====================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    pause
    exit /b 1
)

echo [1/4] Verification de Python... OK
echo.

REM Installer PyInstaller si nécessaire
echo [2/4] Installation de PyInstaller...
pip install pyinstaller requests
echo.

REM Créer l'icône si elle n'existe pas
if not exist "assets\icon.ico" (
    echo [INFO] Pas d'icone trouvee, l'exe n'aura pas d'icone
)

REM Compiler le launcher
echo [3/4] Compilation du launcher...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name VoiceSnap ^
    --icon assets\icon.ico ^
    --add-data "python;python" ^
    --add-data "src;src" ^
    --add-data "src-tauri;src-tauri" ^
    --add-data "package.json;." ^
    --add-data "index.html;." ^
    launcher.py

if errorlevel 1 (
    echo.
    echo [ERREUR] La compilation a echoue
    pause
    exit /b 1
)

echo.
echo [4/4] Nettoyage...
rmdir /s /q build
del VoiceSnap.spec

echo.
echo ====================================
echo   BUILD TERMINE !
echo ====================================
echo.
echo Executable cree : dist\VoiceSnap.exe
echo.
echo Pour lancer l'application :
echo   1. Double-cliquez sur dist\VoiceSnap.exe
echo   2. Le backend Python et l'interface Tauri vont demarrer
echo.
pause
