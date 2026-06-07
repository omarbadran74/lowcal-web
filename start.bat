@echo off
set PYTHONUTF8=1
echo Starting LowCal server on http://127.0.0.1:8001
echo Admin: admin / admin123
echo Cashier: cashier / cashier123
C:\tmp\python312\python.exe manage.py runserver 8001
pause
