from datetime import datetime

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton


class ConsoleBasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.success_count = 0
        self.fail_count = 0
        self.is_running = False
        self.log_count = 0
        self.init_ui()

    def init_ui(self):

        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        # 顶部状态栏
        status_layout = QHBoxLayout()
        status_layout.setSpacing(20)  # 设置组件之间的间距

        # 统一标签样式
        label_style = """
            QLabel {
                font-family: 'Microsoft YaHei';
                font-size: 14px;
                padding: 5px 15px;
                border-radius: 4px;
                min-width: 100px;
                text-align: center;
                background-color: #f5f5f5;
            }
        """

        # 成功数量标签
        self.success_label = QLabel(f'成功: {self.success_count}')
        self.success_label.setStyleSheet(label_style + """
            QLabel {
                background-color: #2e7d32;
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #81c784;
            }
        """)

        # 失败数量标签
        self.fail_label = QLabel(f'失败: {self.fail_count}')
        self.fail_label.setStyleSheet(label_style + """
            QLabel {
                background-color: #c62828;
                color: #ffffff;
                border: 1px solid #e57373;
                font-weight: bold;
            }
        """)

        # 运行状态标签
        self.status_label = QLabel('未运行')
        self.status_label.setStyleSheet(label_style + """
            QLabel {
                background-color: #616161;
                color: #ffffff;     
                font-weight: bold;       
                border: 1px solid #bdbdbd;
            }
        """)

        status_layout.addWidget(self.success_label)
        status_layout.addWidget(self.fail_label)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        # 控制台窗口
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Consolas, Monaco, monospace;
                padding: 10px;
                border: none;
            }
        """)

        # 底部按钮栏
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # 启动/停止按钮
        self.start_stop_button = QPushButton('启动')
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.start_stop_button.clicked.connect(self.toggle_start_stop)

        # 清空日志按钮
        self.clear_button = QPushButton('清空日志')
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        """)
        self.clear_button.clicked.connect(self.clear_console)

        button_layout.addWidget(self.start_stop_button)
        button_layout.addWidget(self.clear_button)

        # 添加所有组件到主布局
        layout.addLayout(status_layout)
        layout.addWidget(self.console)
        layout.addLayout(button_layout)

    def toggle_start_stop(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.start_stop_button.setText('停止')
            self.start_stop_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 14px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e53935;
                }
                QPushButton:pressed {
                    background-color: #d32f2f;
                }
            """)
            self.status_label.setText('运行中')
            self.status_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-weight: bold;
                    border: 1px solid blue;
                    ont-family: 'Microsoft YaHei';
                    font-size: 14px;
                    padding: 5px 15px;
                    border-radius: 4px;
                    min-width: 100px;
                    text-align: center;
                    background-color: blue;
                }
            """)
        else:
            self.start_stop_button.setText('启动')
            self.start_stop_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 14px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)
            self.status_label.setText('未运行')
            self.status_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-weight: bold;
                    border: 1px solid #bdbdbd;
                    ont-family: 'Microsoft YaHei';
                    font-size: 14px;
                    padding: 5px 15px;
                    border-radius: 4px;
                    min-width: 100px;
                    text-align: center;
                    background-color: #616161;
                }
            """)

    def clear_console(self):
        self.console.clear()

    def log(self, message, log_type='info'):
        info = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] "
        # 根据日志类型设置颜色
        if log_type == 'success':
            colored_message = f'<span style="color: #2e7d32;">{info + message}</span>'
        elif log_type == 'fail':
            colored_message = f'<span style="color: #c62828;">{info + message}</span>'
        elif log_type == 'warn':
            colored_message = f'<span style="color: #FFA200;">{info + message}</span>'
        else:
            colored_message = info + message

        self.console.append(colored_message)
        self.log_count += 1

        # 当日志数量超过120条时，清除前60条
        if self.log_count > 120:
            text = self.console.toPlainText()
            lines = text.split('\n')
            self.console.clear()
            self.console.append('\n'.join(lines[60:]))
            self.log_count -= 60

    def update_success_count(self, count):
        self.success_count = count
        self.success_label.setText(f'成功: {self.success_count}')

    def update_fail_count(self, count):
        self.fail_count = count
        self.fail_label.setText(f'失败: {self.fail_count}')
