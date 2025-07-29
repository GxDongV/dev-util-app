from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout, QLabel, QStackedWidget, QGroupBox)
from PyQt5.QtCore import Qt
from tools.name_converter import NameConverter
from tools.json_formatter import JsonFormatTool
from tools.xml_formatter import XmlFormatTool

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("开发工具集")
        self.setGeometry(100, 100, 1000, 700)

        # 创建中心部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 创建侧边栏
        sidebar = QWidget()
        sidebar.setFixedWidth(150)
        sidebar_layout = QVBoxLayout(sidebar)

        # 直接添加工具按钮（移除分组框）
        self.name_convert_btn = QPushButton("命名转换")
        self.json_format_btn = QPushButton("JSON格式转换")
        self.xml_format_btn = QPushButton("XML格式转换")

        # 添加按钮到侧边栏
        sidebar_layout.addWidget(self.name_convert_btn)
        sidebar_layout.addWidget(self.json_format_btn)
        sidebar_layout.addWidget(self.xml_format_btn)
        sidebar_layout.addStretch()

        # 创建主内容区域
        main_content = QWidget()
        main_content_layout = QVBoxLayout(main_content)

        # 添加标签显示
        self.tab_label = QLabel("当前工具: 命名转换")
        self.tab_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # 创建顶部水平布局
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.tab_label)
        top_layout.addStretch()  # 右侧添加伸缩空间，将标签推到左侧

        # 创建堆叠窗口
        self.stack = QStackedWidget()

        # 添加到主内容布局
        main_content_layout.addLayout(top_layout)
        main_content_layout.addWidget(self.stack)

        # 初始化所有工具界面
        self.init_tools()

        # 设置布局比例
        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(main_content, 4)

        # 连接按钮事件
        self.connect_signals()

    def init_tools(self):
        """初始化所有工具界面"""
        # 创建工具实例
        self.name_converter = NameConverter()
        self.json_formatter = JsonFormatTool()
        self.xml_formatter = XmlFormatTool()

        
        # 将所有界面添加到stack
        self.stack.addWidget(self.name_converter)        # 0: 命名转换
        self.stack.addWidget(self.json_formatter)        # 1: JSON格式转换
        self.stack.addWidget(self.xml_formatter)         # 3: XML格式转换

    def create_generic_interface(self, title):
        """创建通用工具界面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(f'{title}功能开发中'))
        return widget

    def connect_signals(self):
        """连接所有按钮信号"""
        # 更新标签并切换界面的辅助函数
        def update_and_switch(index, title):
            self.stack.setCurrentIndex(index)
            self.tab_label.setText(f"当前工具: {title}")

        # 连接按钮事件
        self.name_convert_btn.clicked.connect(lambda: update_and_switch(0, "命名转换"))
        self.json_format_btn.clicked.connect(lambda: update_and_switch(1, "JSON格式转换"))
        self.xml_format_btn.clicked.connect(lambda: update_and_switch(2, "XML格式转换"))

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())