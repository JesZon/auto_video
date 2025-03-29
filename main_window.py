import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QApplication, \
    QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from pages.ai_article_page import AIArticlePage
from pages.comfyui_page import ComfyUIPage
from pages.jianying_page import JianYingPage
from pages.settings_page import SettingsPage
from auto_operate import get_config, set_config

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller会创建临时文件夹并将资源文件存放在_MEIPASS中
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pages = None
        self.content_stack = None
        self.nav_list = None
        self.init_ui()
        self.setWindowFlags(self.windowFlags())

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle('图文小说自动化剪辑工具')
        self.resize(950, 650)
        self.setFixedSize(950, 650)

        # 设置应用图标
        self.setWindowIcon(QIcon(resource_path('public/scissors-cut-fill.ico')))

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #2971CF;
            }
        """)

        # 创建水平布局
        layout = QHBoxLayout(central_widget)

        # 创建左侧导航栏
        self.nav_list = QListWidget()
        self.nav_list.setMaximumWidth(150)  # 设置导航栏最大宽度

        # 设置导航栏样式
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: #052F78;
                border: none;
                outline: none;
                padding: 0;
                border-radius: 0;
                font-weight: bold;
                font-size: 14px;
            }
            QListWidget::item {
                color: #ffffff;
                padding: 10px;
                margin: 0;
                border-radius: 0;
                height: 20px;
                line-height: 20px;
                border-bottom: 1px solid #C6E8FE;
            }
            QListWidget::item:has-icon {
                padding-left: 10px;
            }
            QListWidget::item:hover {
                background-color: #7DC1FC;
            }
            QListWidget::item:selected {
                background-color: #3C7EFF;
                color: #ffffff;
            }
        """)

        # 添加导航项
        nav_items = ['设置', 'AI文章', 'Comfyui出图', '剪映自动化']

        # 创建右侧内容区域
        self.content_stack = QStackedWidget()

        # 添加页面到堆栈
        self.pages = {
            '设置': SettingsPage(),
            'AI文章': AIArticlePage(),
            'Comfyui出图': ComfyUIPage(),
            '剪映自动化': JianYingPage()
        }

        for page_name, page_widget in self.pages.items():
            self.content_stack.addWidget(page_widget)

        # 添加导航项
        for item_text in nav_items:
            item = QListWidgetItem(item_text)
            item.setTextAlignment(Qt.AlignLeft)
            # 为设置项添加图标
            if item_text == '设置':
                icon = QIcon(resource_path('public/setting.svg'))
                item.setIcon(icon)
            self.nav_list.addItem(item)

        # 连接导航项点击事件
        self.nav_list.currentRowChanged.connect(self.switch_page)
        self.nav_list.setCurrentRow(0)  # 默认选中第一项

        # 添加到布局
        layout.addWidget(self.nav_list)
        layout.addWidget(self.content_stack)

    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)

    def closeEvent(self, event):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('确认关闭')
        msg_box.setText('你确定要关闭窗口吗？')
        yes_button = msg_box.addButton('是', QMessageBox.YesRole)
        no_button = msg_box.addButton('否', QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            # 准备要保存的配置
            config = {
                "theme": get_config()["theme"],
                "api_key": get_config()["api_key"],
                "base_url": get_config()["base_url"],
                "jianying_draft": get_config()["jianying_draft"],
                "jianying_draft_update": False,
            }
            set_config(config)
            event.accept()  # 接受关闭事件
        else:
            event.ignore()  # 忽略关闭事件


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("QMessageBox QPushButton { text: '是' }")
    app.setStyleSheet("QMessageBox QPushButton:last-child { text: '否' }")
    window = MainWindow()
    window.setWindowFlags(window.windowFlags())
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
# {
#     "theme": 0,
#     "api_key": "sk-e0bb19eccb0f4b7a814e50d1b7f9add5",
#     "base_url": "https://api.deepseek.com",
#     "jianying_draft": "D:/softwareInstall/JianyingPro Drafts"
# }
# 打包 pyinstaller --noconfirm --clean main_window.spec