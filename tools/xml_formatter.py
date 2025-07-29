# tools/xml_converter.py
from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QWidget
from .base_tool import BaseTool


class XmlFormatter(BaseTool):
    def __init__(self):
        super().__init__("XML转换工具")

    def init_ui(self):
        """
        重写init_ui方法，创建独立的UI布局
        """
        layout = QVBoxLayout()

        # 创建水平布局用于分开展示
        h_layout = QHBoxLayout()

        # 左侧输入区域
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("请输入XML内容...")
        h_layout.addWidget(self.input_area)

        # 右侧输出区域
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setPlaceholderText("转换结果将显示在这里...")
        h_layout.addWidget(self.output_area)

        layout.addLayout(h_layout)

        # 转换按钮
        self.convert_btn = QPushButton("转换XML")
        self.convert_btn.clicked.connect(self.format_content)
        layout.addWidget(self.convert_btn)

        self.setLayout(layout)

    def format_content(self):
        """
        实现XML格式化逻辑
        """
        input_text = self.input_area.toPlainText()
        if not input_text.strip():
            self.output_area.setPlainText("请输入XML内容")
            return

        try:
            # 这里实现具体的XML转换逻辑
            # 示例：简单的XML格式化
            import xml.dom.minidom
            dom = xml.dom.minidom.parseString(input_text)
            formatted_xml = dom.toprettyxml(indent="  ")
            # 移除XML声明前的空行
            formatted_xml = '\n'.join(line for line in formatted_xml.split('\n') if line.strip())
            self.output_area.setPlainText(formatted_xml)
        except Exception as e:
            self.output_area.setPlainText(f"XML格式错误: {str(e)}")

    def process(self, text: str):
        """
        实现BaseTool的抽象方法
        """
        # 这里可以实现更复杂的XML处理逻辑
        return text  # 简化示例
