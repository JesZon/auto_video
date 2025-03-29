import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QScrollArea, QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
from qfluentwidgets import ComboBox, CaptionLabel, LineEdit, PrimaryPushButton, InfoBarIcon, \
    FlyoutAnimationType, Flyout
import os
import shutil
import auto_operate
from auto_operate import __ai_article_path__


def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller会创建临时文件夹并将资源文件存放在_MEIPASS中
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 关键设置：允许内容自动调整大小
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条

        # 创建内容容器（所有内容放在这个容器中）
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)  # 添加适当边距

        # 将原来的主布局改为使用内容容器的布局
        layout = content_layout  # 注意这里将原来的layout变量指向content_layout

        # 以下是原始布局代码（保持原有逻辑，仅将布局操作对象改为content_layout）
        # ---------------------- 原始代码开始 ----------------------

        # 主题选择区域
        theme_layout = QHBoxLayout()
        caption_label = CaptionLabel("主题：")
        caption_label.setStyleSheet("""
            font-size: 16px;
            color: #fff;
        """)
        theme_layout.addWidget(caption_label)
        comboBox = ComboBox()
        items = ['蓝色', '深色', '浅色']
        comboBox.addItems(items)
        comboBox.setText(items[auto_operate.get_config()["theme"]])
        theme_layout.addWidget(comboBox)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        # API Key区域
        api_key_layout = QHBoxLayout()
        api_key_label = CaptionLabel("API Key：")
        api_key_label.setStyleSheet("""
            font-size: 16px;
            color: #fff;
        """)
        api_key_layout.addWidget(api_key_label)
        line_edit = LineEdit()
        line_edit.setText(auto_operate.get_config()["api_key"])
        api_key_layout.addWidget(line_edit)
        api_key_layout.addStretch()
        layout.addLayout(api_key_layout)

        # Base URL区域
        base_url_layout = QHBoxLayout()
        base_url_label = CaptionLabel("Base URL：")
        base_url_label.setStyleSheet("""
            font-size: 16px;
            color: #fff;
        """)
        base_url_layout.addWidget(base_url_label)
        line_edit = LineEdit()
        line_edit.setText(auto_operate.get_config()["base_url"])
        base_url_layout.addWidget(line_edit)
        base_url_layout.addStretch()
        layout.addLayout(base_url_layout)

        # 剪映草稿文件夹
        draft_layout = QHBoxLayout()
        draft_label = CaptionLabel("剪映草稿文件夹：")
        draft_label.setStyleSheet("""
            font-size: 16px;
            color: #fff;
        """)
        draft_layout.addWidget(draft_label)
        # 添加输入框和选择按钮
        self.draft_path_edit = LineEdit()
        self.draft_path_edit.setText(auto_operate.get_config()["jianying_draft"])
        draft_layout.addWidget(self.draft_path_edit)
        prim_button = PrimaryPushButton('选择文件夹')
        prim_button.clicked.connect(self.select_draft_folder)
        draft_layout.addWidget(prim_button)
        draft_layout.addStretch()
        layout.addLayout(draft_layout)

        # 多文件选择区域
        self.multi_files_layout = QHBoxLayout()
        multi_files_label = CaptionLabel("文章导入：")
        multi_files_label.setStyleSheet("""
            font-size: 16px;
            color: #fff;
        """)
        self.multi_files_layout.addWidget(multi_files_label)
        self.multi_files_button = PrimaryPushButton('选择文件')
        self.multi_files_button.clicked.connect(self.select_multiple_files)
        self.multi_files_layout.addWidget(self.multi_files_button)
        self.multi_files_layout.addStretch()
        layout.addLayout(self.multi_files_layout)

        # 保存按钮区域
        self.save_button = PrimaryPushButton('保存设置')
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        # 添加警告提示区域
        warning_layout = QHBoxLayout()
        warning_layout.setContentsMargins(0, 8, 0, 0)
        warning_layout.setSpacing(8)

        # 添加警告图标
        warning_icon = QLabel()
        warning_icon.setFixedSize(16, 16)
        warning_icon.setPixmap(QPixmap(resource_path('public/warn.svg')).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        warning_layout.addWidget(warning_icon)

        # 添加警告文字
        warning_text = QLabel('修改了剪映草稿文件夹路径需重启软件才能生效。')
        warning_text.setStyleSheet('color: #FAAD14; font-size: 15px;')
        warning_layout.addWidget(warning_text)
        warning_layout.addStretch()

        layout.addLayout(warning_layout)
        layout.addStretch()
        layout.addStretch()
        # ---------------------- 原始代码结束 ----------------------

        # 设置滚动区域内容
        scroll_area.setWidget(self.content_widget)

        # 将滚动区域设置为主窗口的主部件
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)

    def select_draft_folder(self):
        current_path = self.draft_path_edit.text()
        folder = QFileDialog.getExistingDirectory(self, "选择剪映草稿文件夹", current_path)
        if folder:
            self.draft_path_edit.setText(folder)

    def select_multiple_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择多个文件", filter="文本文件 (*.txt)")
        if files:
            copied_files = []
            for file in files:
                target_file = os.path.join(__ai_article_path__, os.path.basename(file))
                shutil.copy2(file, target_file)
                copied_files.append(target_file)
            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title="成功",
                content="文件导入成功！",
                target=self.multi_files_button,
                parent=self.content_widget,
                isClosable=False,
                aniType=FlyoutAnimationType.FADE_IN
            )

    def save_settings(self):
        # 获取当前设置值
        theme = self.findChild(ComboBox).currentText()
        switch = {
            '蓝色': 0,
            '深色': 1,
            '浅色': 2
        }
        theme_index = switch.get(theme, 0)
        api_key = self.findChildren(LineEdit)[0].text()
        base_url = self.findChildren(LineEdit)[1].text()
        jianying_draft = self.draft_path_edit.text()

        # 获取原始配置
        old_config = auto_operate.get_config()
        old_jianying_draft = old_config['jianying_draft']

        jianying_draft_update = False
        # 如果剪映草稿文件夹路径发生变化，关闭软件
        if old_jianying_draft != jianying_draft:
            jianying_draft_update = True

        # 准备要保存的配置
        config = {
            "theme": theme_index,
            "api_key": api_key,
            "base_url": base_url,
            "jianying_draft": jianying_draft,
            "jianying_draft_update": jianying_draft_update
        }
        auto_operate.set_config(config)

        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title="成功",
            content="配置保存成功！",
            target=self.save_button,
            parent=self.content_widget,
            isClosable=False,
            aniType=FlyoutAnimationType.FADE_IN
        )
