#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频转GIF工具 - 核心转换模块
"""
import os
import sys
from pathlib import Path
from moviepy.editor import VideoFileClip


class QualitySettings:
    """质量配置类"""
    HIGH = {
        'fps': 15,
        'scale': 1.0,
        'optimize': True,
        'colors': 256
    }
    MEDIUM = {
        'fps': 10,
        'scale': 0.75,
        'optimize': True,
        'colors': 128
    }
    LOW = {
        'fps': 8,
        'scale': 0.5,
        'optimize': True,
        'colors': 64
    }


class VideoToGifConverter:
    """视频转GIF转换器"""

    SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v']

    def __init__(self, input_dir='D:/GIF/start', output_dir='D:/GIF/finish'):
        """
        初始化转换器
        :param input_dir: 输入视频文件夹
        :param output_dir: 输出GIF文件夹
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self._ensure_dirs()

    def _ensure_dirs(self):
        """确保输入输出目录存在"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        if not self.input_dir.exists():
            self.input_dir.mkdir(parents=True, exist_ok=True)

    def get_video_files(self):
        """获取所有支持的视频文件"""
        video_files = []
        if self.input_dir.exists():
            for file in self.input_dir.iterdir():
                if file.is_file() and file.suffix.lower() in self.SUPPORTED_FORMATS:
                    video_files.append(file)
        return sorted(video_files)

    def convert_single(self, video_path, quality='medium', progress_callback=None):
        """
        转换单个视频文件为GIF
        :param video_path: 视频文件路径
        :param quality: 质量等级 ('high', 'medium', 'low')
        :param progress_callback: 进度回调函数
        :return: (成功标志, 输出文件路径或错误信息)
        """
        try:
            video_path = Path(video_path)
            output_filename = video_path.stem + '.gif'
            output_path = self.output_dir / output_filename

            # 获取质量配置
            quality_settings = self._get_quality_settings(quality)

            if progress_callback:
                progress_callback(f"正在加载视频: {video_path.name}")

            # 加载视频
            clip = VideoFileClip(str(video_path))

            # 应用缩放
            if quality_settings['scale'] != 1.0:
                new_width = int(clip.w * quality_settings['scale'])
                new_height = int(clip.h * quality_settings['scale'])
                clip = clip.resize((new_width, new_height))

            if progress_callback:
                progress_callback(f"正在转换: {video_path.name}")

            # 转换为GIF
            clip.write_gif(
                str(output_path),
                fps=quality_settings['fps'],
                program='ffmpeg',
                opt='nq',
                colors=quality_settings['colors']
            )

            clip.close()

            if progress_callback:
                progress_callback(f"完成: {output_filename}")

            return True, str(output_path)

        except Exception as e:
            error_msg = f"转换失败 {video_path.name}: {str(e)}"
            if progress_callback:
                progress_callback(error_msg)
            return False, error_msg

    def convert_batch(self, quality='medium', progress_callback=None):
        """
        批量转换所有视频文件
        :param quality: 质量等级
        :param progress_callback: 进度回调函数
        :return: (成功数量, 失败数量, 结果列表)
        """
        video_files = self.get_video_files()
        total = len(video_files)

        if total == 0:
            if progress_callback:
                progress_callback("未找到视频文件!")
            return 0, 0, []

        if progress_callback:
            progress_callback(f"找到 {total} 个视频文件,开始转换...")

        success_count = 0
        fail_count = 0
        results = []

        for idx, video_file in enumerate(video_files, 1):
            if progress_callback:
                progress_callback(f"\n处理 [{idx}/{total}]: {video_file.name}")

            success, result = self.convert_single(video_file, quality, progress_callback)

            if success:
                success_count += 1
            else:
                fail_count += 1

            results.append({
                'file': video_file.name,
                'success': success,
                'result': result
            })

        if progress_callback:
            progress_callback(f"\n转换完成! 成功: {success_count}, 失败: {fail_count}")

        return success_count, fail_count, results

    def _get_quality_settings(self, quality):
        """获取质量配置"""
        quality_map = {
            'high': QualitySettings.HIGH,
            'medium': QualitySettings.MEDIUM,
            'low': QualitySettings.LOW
        }
        return quality_map.get(quality.lower(), QualitySettings.MEDIUM)


if __name__ == '__main__':
    # 测试代码
    converter = VideoToGifConverter()

    def print_progress(msg):
        print(msg)

    print("开始批量转换...")
    success, fail, results = converter.convert_batch(quality='medium', progress_callback=print_progress)
    print(f"\n总计: 成功 {success}, 失败 {fail}")
