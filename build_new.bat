@echo off
chcp 65001 >nul
echo ========================================
echo 视频转GIF工具 - 一键打包脚本
echo ========================================
echo.

echo [步骤 1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python
    echo 请从 https://www.python.org/downloads/ 下载安装Python 3.7或更高版本
    echo.
    pause
    exit /b 1
)
python --version
echo.

echo [步骤 2/3] 安装依赖库...
echo 正在安装: moviepy, Pillow, PyQt5, pyinstaller
echo 这可能需要几分钟时间,请耐心等待...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo 错误: 依赖安装失败
    echo 请检查网络连接或尝试使用镜像源:
    echo python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo.
    pause
    exit /b 1
)
echo.
echo 依赖安装完成!
echo.

echo [步骤 3/3] 执行打包...
echo 使用调试版打包脚本,将显示详细信息
echo.
python build_exe_debug.py
if errorlevel 1 (
    echo.
    echo 打包过程遇到错误
    echo 请查看上面的错误信息
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包流程完成!
echo ========================================
echo.
echo 可执行文件位置: fin\VideoToGIF.exe
echo.
pause
