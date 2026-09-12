@echo off
chcp 65001 >nul
title Smart Clinic - 智能门诊医生工作站
echo.
echo ========================================
echo   Smart Clinic - 智能门诊医生工作站
echo ========================================
echo.
echo 正在启动服务...
echo.
start http://127.0.0.1:5000
python app.py
pause
