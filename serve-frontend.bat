@echo off
echo Serving frontend at http://127.0.0.1:5500
echo Open in browser and ensure API is running on port 8000
cd /d "%~dp0src"
python -m http.server 5500
