#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 带详细调试信息的版本
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path


def check_dependencies():
    """检查所有依赖是否已安装"""
    print("\n[检查依赖]")
    required_modules = {
        'PyInstaller': 'pyinstaller',
        'moviepy': 'moviepy',
        'PIL': 'Pillow',
        'PyQt5': 'PyQt5'
    }

    missing = []
    for module, package in required_modules.items():
        try:
            __import__(module)
            print(f"  ✓ {package} 已安装")
        except ImportError:
            print(f"  ✗ {package} 未安装")
            missing.append(package)

    if missing:
        print(f"\n缺少依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False

    return True


def check_files():
    """检查必要的源文件是否存在"""
    print("\n[检查源文件]")
    required_files = ['gui.py', 'video_to_gif.py', 'requirements.txt']

    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file} 存在")
        else:
            print(f"  ✗ {file} 不存在")
            all_exist = False

    return all_exist


def main():
    """执行打包"""
    print("=" * 70)
    print("视频转GIF工具 - 打包脚本 (调试版)")
    print("=" * 70)

    # 检查Python版本
    print(f"\nPython版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")

    # 检查源文件
    if not check_files():
        print("\n错误: 缺少必要的源文件")
        input("\n按回车键退出...")
        return False

    # 检查依赖
    if not check_dependencies():
        print("\n是否现在安装依赖? (y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            print("\n正在安装依赖...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
                print("依赖安装完成!")
            except Exception as e:
                print(f"依赖安装失败: {e}")
                input("\n按回车键退出...")
                return False
        else:
            input("\n按回车键退出...")
            return False

    # 清理旧的构建文件
    print("\n[清理旧文件]")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  ✓ 已删除: {dir_name}")
            except Exception as e:
                print(f"  ! 删除失败 {dir_name}: {e}")

    # 删除旧的spec文件
    spec_files = ['VideoToGIF.spec', 'gui.spec']
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            try:
                os.remove(spec_file)
                print(f"  ✓ 已删除: {spec_file}")
            except Exception as e:
                print(f"  ! 删除失败 {spec_file}: {e}")

    # 执行打包
    print("\n[开始打包]")
    print("这可能需要几分钟时间,请耐心等待...")
    print("-" * 70)

    cmd = [
        sys.executable,
        '-m',
        'PyInstaller',
        '--name=VideoToGIF',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        'gui.py'
    ]

    print(f"执行命令: {' '.join(cmd)}\n")

    try:
        # 直接显示输出,不捕获
        result = subprocess.run(cmd, check=True)
        print("\n" + "-" * 70)
        print("打包命令执行成功!")
    except subprocess.CalledProcessError as e:
        print("\n" + "-" * 70)
        print(f"打包失败! 错误代码: {e.returncode}")
        input("\n按回车键退出...")
        return False
    except Exception as e:
        print("\n" + "-" * 70)
        print(f"打包过程出错: {e}")
        input("\n按回车键退出...")
        return False

    # 检查生成的文件
    print("\n[检查输出文件]")
    exe_source = Path('dist/VideoToGIF.exe')

    if not exe_source.exists():
        print(f"  ✗ 未找到: {exe_source}")
        print("\n可能的原因:")
        print("  1. PyInstaller打包失败")
        print("  2. 缺少必要的依赖库")
        print("  3. 杀毒软件拦截了exe文件")
        print("\n请检查上面的输出信息中是否有错误提示")

        # 检查dist目录
        if os.path.exists('dist'):
            dist_files = list(Path('dist').glob('*'))
            if dist_files:
                print(f"\ndist目录中的文件:")
                for f in dist_files:
                    print(f"  - {f.name}")
            else:
                print("\ndist目录为空")
        else:
            print("\ndist目录不存在")

        input("\n按回车键退出...")
        return False

    file_size_mb = exe_source.stat().st_size / (1024 * 1024)
    print(f"  ✓ 找到exe文件: {exe_source}")
    print(f"  文件大小: {file_size_mb:.2f} MB")

    # 移动到fin文件夹
    print("\n[复制到fin文件夹]")
    fin_dir = Path('fin')
    fin_dir.mkdir(exist_ok=True)
    exe_dest = fin_dir / 'VideoToGIF.exe'

    try:
        shutil.copy2(exe_source, exe_dest)
        print(f"  ✓ 已复制到: {exe_dest.absolute()}")
        print(f"  文件大小: {file_size_mb:.2f} MB")
    except Exception as e:
        print(f"  ✗ 复制失败: {e}")
        input("\n按回车键退出...")
        return False

    # 清理临时文件
    print("\n[清理临时文件]")
    if os.path.exists('build'):
        try:
            shutil.rmtree('build')
            print("  ✓ 已删除: build")
        except Exception as e:
            print(f"  ! 删除失败: {e}")

    if os.path.exists('VideoToGIF.spec'):
        try:
            os.remove('VideoToGIF.spec')
            print("  ✓ 已删除: VideoToGIF.spec")
        except Exception as e:
            print(f"  ! 删除失败: {e}")

    # 完成
    print("\n" + "=" * 70)
    print("打包完成!")
    print("=" * 70)
    print(f"\n可执行文件位置: {exe_dest.absolute()}")
    print("\n你现在可以:")
    print("  1. 运行 fin\\VideoToGIF.exe 测试程序")
    print("  2. 将 VideoToGIF.exe 分发给其他用户")
    print("=" * 70)

    input("\n按回车键退出...")
    return True


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        sys.exit(1)
