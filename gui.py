#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频转GIF工具 - 图形用户界面
"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QComboBox, QGroupBox,
    QFileDialog, QLineEdit, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from video_to_gif import VideoToGifConverter


class ConvertThread(QThread):
    """转换线程"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(int, int)

    def __init__(self, converter, quality):
        super().__init__()
        self.converter = converter
        self.quality = quality

    def run(self):
        """执行转换"""
        success, fail, results = self.converter.convert_batch(
            quality=self.quality,
            progress_callback=self.emit_progress
        )
        self.finished.emit(success, fail)

    def emit_progress(self, msg):
        """发送进度信息"""
        self.progress.emit(msg)


class VideoToGifGUI(QMainWindow):
    """视频转GIF工具主窗口"""

    def __init__(self):
        super().__init__()
        self.converter = None
        self.convert_thread = None
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle('视频转GIF工具 v1.0')
        self.setGeometry(100, 100, 800, 600)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 标题
        title = QLabel('批量视频转GIF工具')
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # 路径设置组
        path_group = QGroupBox('路径设置')
        path_layout = QVBoxLayout()

        # 输入路径
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel('输入文件夹:'))
        self.input_path_edit = QLineEdit('D:/GIF/start')
        input_layout.addWidget(self.input_path_edit)
        self.input_browse_btn = QPushButton('浏览...')
        self.input_browse_btn.clicked.connect(self.browse_input_dir)
        input_layout.addWidget(self.input_browse_btn)
        path_layout.addLayout(input_layout)

        # 输出路径
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel('输出文件夹:'))
        self.output_path_edit = QLineEdit('D:/GIF/finish')
        output_layout.addWidget(self.output_path_edit)
        self.output_browse_btn = QPushButton('浏览...')
        self.output_browse_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(self.output_browse_btn)
        path_layout.addLayout(output_layout)

        path_group.setLayout(path_layout)
        main_layout.addWidget(path_group)

        # 质量设置组
        quality_group = QGroupBox('转换设置')
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel('输出质量:'))

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(['高质量(文件较大)', '中等质量(推荐)', '低质量(文件较小)'])
        self.quality_combo.setCurrentIndex(1)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()

        quality_group.setLayout(quality_layout)
        main_layout.addWidget(quality_group)

        # 操作按钮
        button_layout = QHBoxLayout()
        self.scan_btn = QPushButton('扫描视频文件')
        self.scan_btn.setMinimumHeight(40)
        self.scan_btn.clicked.connect(self.scan_videos)
        button_layout.addWidget(self.scan_btn)

        self.convert_btn = QPushButton('开始转换')
        self.convert_btn.setMinimumHeight(40)
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setEnabled(False)
        button_layout.addWidget(self.convert_btn)

        main_layout.addLayout(button_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # 日志输出
        log_label = QLabel('转换日志:')
        main_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(200)
        main_layout.addWidget(self.log_text)

        # 状态栏
        self.statusBar().showMessage('就绪')

        # 添加版权信息
        copyright_label = QLabel('MonkeyCode-AI 智能开发平台')
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet('color: gray; font-size: 10px;')
        main_layout.addWidget(copyright_label)

    def browse_input_dir(self):
        """浏览输入目录"""
        directory = QFileDialog.getExistingDirectory(
            self,
            '选择视频输入文件夹',
            self.input_path_edit.text()
        )
        if directory:
            self.input_path_edit.setText(directory)
            self.log('已选择输入文件夹: ' + directory)

    def browse_output_dir(self):
        """浏览输出目录"""
        directory = QFileDialog.getExistingDirectory(
            self,
            '选择GIF输出文件夹',
            self.output_path_edit.text()
        )
        if directory:
            self.output_path_edit.setText(directory)
            self.log('已选择输出文件夹: ' + directory)

    def scan_videos(self):
        """扫描视频文件"""
        input_dir = self.input_path_edit.text()
        output_dir = self.output_path_edit.text()

        # 创建转换器实例
        self.converter = VideoToGifConverter(input_dir, output_dir)

        # 获取视频文件
        video_files = self.converter.get_video_files()

        if not video_files:
            self.log('未找到视频文件!')
            QMessageBox.warning(self, '警告', f'在 {input_dir} 中未找到支持的视频文件!')
            self.convert_btn.setEnabled(False)
            return

        # 显示扫描结果
        self.log(f'\n找到 {len(video_files)} 个视频文件:')
        for video in video_files:
            file_size = video.stat().st_size / (1024 * 1024)
            self.log(f'  - {video.name} ({file_size:.2f} MB)')

        self.convert_btn.setEnabled(True)
        self.statusBar().showMessage(f'已找到 {len(video_files)} 个视频文件')

    def start_conversion(self):
        """开始转换"""
        if not self.converter:
            QMessageBox.warning(self, '警告', '请先扫描视频文件!')
            return

        # 获取质量设置
        quality_index = self.quality_combo.currentIndex()
        quality_map = {0: 'high', 1: 'medium', 2: 'low'}
        quality = quality_map[quality_index]

        # 禁用按钮
        self.convert_btn.setEnabled(False)
        self.scan_btn.setEnabled(False)
        self.input_browse_btn.setEnabled(False)
        self.output_browse_btn.setEnabled(False)
        self.quality_combo.setEnabled(False)

        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度

        self.log(f'\n开始批量转换 (质量: {self.quality_combo.currentText()})...')
        self.statusBar().showMessage('正在转换...')

        # 创建并启动转换线程
        self.convert_thread = ConvertThread(self.converter, quality)
        self.convert_thread.progress.connect(self.on_progress)
        self.convert_thread.finished.connect(self.on_finished)
        self.convert_thread.start()

    def on_progress(self, msg):
        """处理进度更新"""
        self.log(msg)

    def on_finished(self, success, fail):
        """转换完成"""
        # 隐藏进度条
        self.progress_bar.setVisible(False)

        # 重新启用按钮
        self.convert_btn.setEnabled(True)
        self.scan_btn.setEnabled(True)
        self.input_browse_btn.setEnabled(True)
        self.output_browse_btn.setEnabled(True)
        self.quality_combo.setEnabled(True)

        # 显示结果
        result_msg = f'转换完成! 成功: {success}, 失败: {fail}'
        self.log(f'\n{result_msg}')
        self.statusBar().showMessage(result_msg)

        # 显示消息框
        QMessageBox.information(self, '完成', result_msg)

    def log(self, message):
        """添加日志"""
        self.log_text.append(message)
        # 滚动到底部
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.End)
        self.log_text.setTextCursor(cursor)


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle('Fusion')

    window = VideoToGifGUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
