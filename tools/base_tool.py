# tools/base_tool.py
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QTextEdit, QPushButton, QVBoxLayout, QWidget
import logging

logger = logging.getLogger(__name__)

from abc import ABCMeta

# 解决元类冲突：合并QWidget和ABCMeta的元类
class Meta(type(QWidget), ABCMeta):
    pass

class BaseTool(QWidget, metaclass=Meta):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.errors = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.input_area = QTextEdit()
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.format_btn = QPushButton("格式化")
        self.format_btn.clicked.connect(self.format_content)

        layout.addWidget(self.input_area)
        layout.addWidget(self.format_btn)
        layout.addWidget(self.output_area)
        self.setLayout(layout)

    @abstractmethod
    def format_content(self):
        """子类需实现具体的格式化逻辑"""
        pass

    # 基类异常处理框架
    def execute(self, text: str):
        try:
            result = self.process(text)
            logger.info(f'{self.name} 执行成功 输入: {text} 输出: {result}')
            return result
        except Exception as e:
            logger.error(f'{self.name} 执行错误: {str(e)}', exc_info=True)
            return (f'处理出错: {str(e)}', '错误')

    def process(self, text: str):
        raise NotImplementedError

    def get_errors(self):
        return self.errors