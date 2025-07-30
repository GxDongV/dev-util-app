# main.py - 主程序入口

import sys
import logging
from ui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import qdarkstyle

logger = logging.getLogger(__name__)

def excepthook(exc_type, exc_value, exc_traceback):
    logger.critical("未捕获异常", exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

if __name__ == "__main__":
    # 全局异常处理配置
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
    )
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    # 默认加载深色主题
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())