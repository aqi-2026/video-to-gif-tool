#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码验证脚本 - 检查Python语法和逻辑
"""
import ast
import sys


def check_syntax(filename):
    """检查Python文件语法"""
    print(f"检查文件: {filename}")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()

        ast.parse(code)
        print(f"  ✓ 语法正确")
        return True
    except SyntaxError as e:
        print(f"  ✗ 语法错误: {e}")
        return False
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("视频转GIF工具 - 代码验证")
    print("=" * 60)
    print()

    files_to_check = [
        'video_to_gif.py',
        'gui.py',
        'build_exe.py'
    ]

    all_passed = True
    for filename in files_to_check:
        if not check_syntax(filename):
            all_passed = False
        print()

    print("=" * 60)
    if all_passed:
        print("所有文件验证通过!")
        print("=" * 60)
        return 0
    else:
        print("部分文件存在问题,请检查")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
