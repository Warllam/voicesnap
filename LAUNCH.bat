@echo off
REM VoiceSnap - Launcher Simple et Robuste
REM Un seul fichier pour tout lancer

title VoiceSnap

color 0A
echo.
echo ========================================
echo      VoiceSnap - Quick Launcher
echo ========================================
echo.

REM Tuer les anciens processus
echo [1] Nettoyage des anciens processus...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq VoiceSnap Backend*" >nul 2>&1
taskkill /F /IM voicesnap.exe >nul 2>&1
timeout /t 1 /nobreak >nul

REM Lancer le backend
echo [2] Demarrage du backend Python...
cd python
start "VoiceSnap Backend" cmd /k "python server.py"
cd ..

REM Attendre 5 secondes
echo [3] Attente du backend (5 secondes)...
timeout /t 5 /nobreak >nul

REM Lancer Tauri
echo [4] Lancement de l'interface...
echo.
echo ========================================
echo    VoiceSnap demarre !
echo ========================================
echo.
echo Backend : http://localhost:8765
echo Interface : http://localhost:1420
echo.
echo Fermez cette fenetre pour tout arreter
echo.

npm run tauri:dev

REM Cleanup
echo.
echo Arret de VoiceSnap...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq VoiceSnap Backend*" >nul 2>&1
taskkill /F /IM voicesnap.exe >nul 2>&1
exit
