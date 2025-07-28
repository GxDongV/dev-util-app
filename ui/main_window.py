from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QHBoxLayout, QLabel, QStackedWidget, QRadioButton)
from PyQt5.QtCore import Qt
from tools.name_converter import NameConverter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name_converter = NameConverter()  # 确保实例化
        self.init_ui()

    def init_ui(self):
        self.stack.addWidget(self.name_converter)
        
        # 输入输出区域
        layout.addWidget(QLabel('输入文本:'))
        self.name_input = QTextEdit()
        layout.addWidget(self.name_input)
        
        convert_btn = QPushButton('自动转换')
        convert_btn.clicked.connect(self.auto_convert_naming)
        layout.addWidget(convert_btn)
        
        layout.addWidget(QLabel('转换结果:'))
        self.name_output = QTextEdit()
        self.name_output.setReadOnly(True)
        layout.addWidget(self.name_output)
        
        return widget

    def auto_convert_naming(self):
        input_text = self.name_input.toPlainText()
        if not self.name_converter.validate_input(input_text):
            self.name_output.setPlainText("输入内容不合法")
            return

        converted_text, convert_type = self.name_converter.process(input_text)
        self.name_output.setPlainText(f"{convert_type}\n{converted_text}")

    def create_json_interface(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 输入区域
        layout.addWidget(QLabel('JSON输入:'))
        self.json_input = QTextEdit()
        layout.addWidget(self.json_input)
        
        # 操作按钮
        format_btn = QPushButton('格式化')
        layout.addWidget(format_btn)
        
        # 输出区域
        layout.addWidget(QLabel('格式化结果:'))
        self.json_output = QTextEdit()
        self.json_output.setReadOnly(True)
        layout.addWidget(self.json_output)
        
        return widget

    def create_xml_interface(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 输入区域
        layout.addWidget(QLabel('XML输入:'))
        self.xml_input = QTextEdit()
        layout.addWidget(self.xml_input)
        
        # 操作按钮
        format_btn = QPushButton('格式化')
        layout.addWidget(format_btn)
        
        # 输出区域
        layout.addWidget(QLabel('格式化结果:'))
        self.xml_output = QTextEdit()
        self.xml_output.setReadOnly(True)
        layout.addWidget(self.xml_output)
        
        return widget

    def format_json(self):
        # 后续添加JSON格式化逻辑
        pass

    def format_xml(self):
        # 后续添加XML格式化逻辑
        pass

    def add_tool(self, tool):
        self.tabs.addTab(tool, tool.name)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())