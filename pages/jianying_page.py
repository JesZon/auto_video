import time

from PyQt5.QtCore import QThread, pyqtSignal, Qt

from auto_operate.jianying_draft import JianYingDraft
from pages.console_base_page import ConsoleBasePage
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget


class JianYingThread(QThread):
    log_info = pyqtSignal(str)
    log_success = pyqtSignal(str)
    log_fail = pyqtSignal(str)
    log_warn = pyqtSignal(str)
    success_signal = pyqtSignal(int)
    fail_signal = pyqtSignal(int)
    start_stop = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_running = True
        self.success_count = 0
        self.fail_count = 0

    def run(self):
        try:
            draft = JianYingDraft((self.log_info, self.log_success, self.log_fail, self.log_warn))
            draft.start()
        except Exception as e:
            self.log_fail.emit(f"剪映自动化进程发生错误: {str(e)}")
        finally:
            time.sleep(1)
            self.is_running = False
            self.start_stop.emit()

    def stop(self):
        self.is_running = False
        self.terminate()
        self.wait()


class JianYingPage(ConsoleBasePage):
    def __init__(self):
        super().__init__()
        self.thread = None
        # 添加警告标签
        self.warning_label = QLabel('剪映自动化进程')
        warning_layout = QHBoxLayout()
        warning_layout.setContentsMargins(0, 0, 0, 0)
        warning_layout.setSpacing(8)
        warning_layout.addWidget(self.warning_label)
        warning_container = QWidget()
        warning_container.setLayout(warning_layout)
        warning_container.setStyleSheet("""
            QLabel {
                color: black;
                font-family: 'Microsoft YaHei';
                font-size: 14px;
                font-weight: bold;
            }
            QWidget {
                padding: 0 8px;
                border-radius: 4px;
                background-color: #f5f5f5;
            }
        """)
        # 在底部按钮栏中添加警告标签
        button_layout = self.layout().itemAt(2).layout()
        button_layout.insertWidget(0, warning_container)
        button_layout.setAlignment(warning_container, Qt.AlignLeft)

    def toggle_start_stop(self):
        super().toggle_start_stop()
        
        if self.is_running:
            # 启动线程
            self.thread = JianYingThread()
            self.thread.log_info.connect(lambda msg: self.log(msg, 'info'))
            self.thread.log_success.connect(lambda msg: self.log(msg, 'success'))
            self.thread.log_fail.connect(lambda msg: self.log(msg, 'fail'))
            self.thread.log_warn.connect(lambda msg: self.log(msg, 'warn'))
            self.thread.success_signal.connect(self.update_success_count)
            self.thread.fail_signal.connect(self.update_fail_count)
            self.thread.start_stop.connect(self.toggle_start_stop)
            self.thread.start()
        else:
            # 停止线程
            if self.thread:
                self.thread.stop()
                self.thread = None