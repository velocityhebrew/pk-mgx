@echo off
title Pokemon AI Challenge - Daily Video Generator & Publisher
cd /d "%~dp0"

echo ======================================================================
echo           POKEMON AI CHALLENGE - AUTONOMOUS GAMING PIPELINE
echo ======================================================================
echo.
echo Running full match generator, TTS dialogue, and publisher...
python daily_runner.py

echo.
echo Pipeline finished.
pause
