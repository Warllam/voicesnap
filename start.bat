@echo off
REM VoiceSnap - Windows Launcher (Simple)
REM Lance le backend Python + l'interface Tauri sans compilation

title VoiceSnap Launcher

echo ====================================
echo   VoiceSnap Launcher v3.0.0
echo ====================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe
    echo Installez Python 3.11+ depuis https://www.python.org/
    pause
    exit /b 1
)

REM Vérifier Node
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Node.js n'est pas installe
    echo Installez Node.js depuis https://nodejs.org/
    pause
    exit /b 1
)

echo [1/3] Verification des dependances... OK
echo.

REM Installer les dépendances Node si nécessaire
if not exist "node_modules\" (
    echo [2/3] Installation des dependances Node...
    call npm install
    echo.
) else (
    echo [2/3] Dependances Node... OK
    echo.
)

REM Démarrer le backend Python en arrière-plan
echo [3/3] Demarrage du backend Python...
start "VoiceSnap Backend" /min python python\server.py

REM Attendre que le serveur soit prêt
echo Attente du serveur backend...
timeout /t 3 /nobreak >nul

REM Vérifier que le backend tourne
curl -s http://localhost:8765/health >nul 2>&1
if errorlevel 1 (
    echo [AVERTISSEMENT] Le backend met du temps a demarrer...
    echo Attendez quelques secondes puis rechargez l'interface si necessaire
    timeout /t 5 /nobreak >nul
)

echo Backend demarre !
echo.

REM Démarrer l'interface Tauri
echo ====================================
echo   VoiceSnap est pret !
echo ====================================
echo.
echo Backend : http://localhost:8765
echo Frontend : http://localhost:1420
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.

REM Lancer Tauri (bloquant)
call npm run tauri:dev

REM Cleanup (si l'utilisateur ferme Tauri)
echo.
echo Arret du backend...
taskkill /FI "WINDOWTITLE eq VoiceSnap Backend*" /F >nul 2>&1

echo.
echo VoiceSnap arrete proprement.
pause
