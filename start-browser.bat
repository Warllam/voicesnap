@echo off
REM VoiceSnap - Launcher navigateur (fallback si Tauri ne marche pas)
REM Lance le backend + ouvre le navigateur sur localhost:1420

title VoiceSnap (Browser Mode)

echo ====================================
echo   VoiceSnap - Mode Navigateur
echo ====================================
echo.

REM Démarrer le backend
echo Demarrage du backend Python...
start "VoiceSnap Backend" /min python python\server.py

REM Attendre un peu
timeout /t 3 /nobreak >nul

REM Démarrer Vite dev server
echo Demarrage du serveur frontend...
start "VoiceSnap Frontend" /min npm run dev

REM Attendre que Vite démarre
echo.
echo Attente du serveur frontend (10 sec)...
timeout /t 10 /nobreak >nul

REM Ouvrir le navigateur
echo.
echo Ouverture du navigateur...
start http://localhost:1420

echo.
echo ====================================
echo   VoiceSnap est pret !
echo ====================================
echo.
echo Backend : http://localhost:8765
echo Frontend : http://localhost:1420
echo.
echo Pour arreter : fermez cette fenetre
echo.
pause
