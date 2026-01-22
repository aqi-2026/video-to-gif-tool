#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将视频转GIF工具打包为exe文件
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    """执行打包"""
    print("=" * 60)
    print("视频转GIF工具 - 打包脚本")
    print("=" * 60)

    # 检查依赖
    print("\n[1/5] 检查依赖...")
    try:
        import PyInstaller
        print("  PyInstaller 已安装")
    except ImportError:
        print("  错误: 未安装 PyInstaller")
        print("  请运行: pip install -r requirements.txt")
        return False

    # 清理旧的构建文件
    print("\n[2/5] 清理旧的构建文件...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  已删除: {dir_name}")

    # 执行打包
    print("\n[3/5] 开始打包...")
    cmd = [
        'pyinstaller',
        '--name=VideoToGIF',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        'gui.py'
    ]

    print(f"  执行命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, text=True)
        print("  打包成功!")
    except subprocess.CalledProcessError as e:
        print(f"  打包失败!")
        print(f"  错误代码: {e.returncode}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"  错误输出: {e.stderr}")
        if hasattr(e, 'stdout') and e.stdout:
            print(f"  标准输出: {e.stdout}")
        return False
    except Exception as e:
        print(f"  打包过程出错: {e}")
        return False

    # 移动exe到fin文件夹
    print("\n[4/5] 移动exe文件到fin文件夹...")
    exe_source = Path('dist/VideoToGIF.exe')
    fin_dir = Path('fin')
    fin_dir.mkdir(exist_ok=True)
    exe_dest = fin_dir / 'VideoToGIF.exe'

    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print(f"  已复制到: {exe_dest}")

        # 获取文件大小
        file_size = exe_dest.stat().st_size / (1024 * 1024)
        print(f"  文件大小: {file_size:.2f} MB")
    else:
        print(f"  错误: 未找到生成的exe文件")
        return False

    # 清理构建临时文件
    print("\n[5/5] 清理临时文件...")
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("  已删除: build")
    if os.path.exists('VideoToGIF.spec'):
        os.remove('VideoToGIF.spec')
        print("  已删除: VideoToGIF.spec")

    print("\n" + "=" * 60)
    print("打包完成!")
    print(f"可执行文件位置: {exe_dest.absolute()}")
    print("=" * 60)

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
