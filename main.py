# main.py - 主程序入口

import sys
import logging
import os
from ui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import qdarkstyle
from qdarkstyle.dark.palette import DarkPalette

logger = logging.getLogger(__name__)

def excepthook(exc_type, exc_value, exc_traceback):
    logger.critical("未捕获异常", exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    # 全局异常处理配置
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
    )
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    
    # 设置应用程序图标
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "app_icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        # 尝试在打包后的资源目录中查找
        try:
            packed_icon_path = get_resource_path("resources/app_icon.ico")
            if os.path.exists(packed_icon_path):
                app.setWindowIcon(QIcon(packed_icon_path))
        except Exception:
            pass  # 如果找不到图标文件，则使用默认图标
    
    # 默认加载深色主题
    app.setStyleSheet(qdarkstyle.load_stylesheet(palette=DarkPalette))
    window = MainWindow()
    
    # 也为窗口设置图标（作为备用）
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    else:
        try:
            packed_icon_path = get_resource_path("resources/app_icon.ico")
            if os.path.exists(packed_icon_path):
                window.setWindowIcon(QIcon(packed_icon_path))
        except Exception:
            pass
    
    window.show()
    sys.exit(app.exec_())