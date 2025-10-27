@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Logo Generator...
echo Open your browser and go to: http://localhost:5000
echo.
python app.py
pause
