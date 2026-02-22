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
start "VoiceSnap Backend" python python\server.py

REM Attendre que le serveur soit prêt (jusqu'à 15 secondes)
echo Attente du serveur backend...
set /a count=0
:wait_backend
timeout /t 1 /nobreak >nul
curl -s http://localhost:8765/health >nul 2>&1
if not errorlevel 1 (
    echo Backend demarre avec succes !
    echo.
    goto backend_ready
)
set /a count+=1
if %count% lss 15 goto wait_backend

echo [AVERTISSEMENT] Le backend met du temps a demarrer...
echo L'application va quand meme demarrer.
echo.

:backend_ready

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
