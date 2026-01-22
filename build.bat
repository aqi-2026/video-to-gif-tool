@echo off
chcp 65001 >nul
echo ========================================
echo 视频转GIF工具 - 一键打包脚本
echo ========================================
echo.

echo [步骤 1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python,请先安装Python 3.7或更高版本
    pause
    exit /b 1
)
python --version
echo.

echo [步骤 2/3] 安装依赖库...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)
echo.

echo [步骤 3/3] 执行打包...
python build_exe.py
if errorlevel 1 (
    echo 错误: 打包失败
    pause
    exit /b 1
)
echo.

echo ========================================
echo 打包完成! exe文件位于 fin 文件夹中
echo ========================================
pause
