# tools/name_converter.py

import logging
from .base_tool import BaseTool
import re
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from .text_context_menu import TextContextMenu
from .find_manager import FindManager

logger = logging.getLogger(__name__)


class NameConverter(BaseTool):
    def __init__(self):
        super().__init__('命名格式转换器')
        self.find_manager = FindManager()

        # 创建输入输出框
        self.input_text = QTextEdit()
        self.input_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.input_text.customContextMenuRequested.connect(self.show_input_context_menu)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setContextMenuPolicy(Qt.CustomContextMenu)
        self.output_area.customContextMenuRequested.connect(self.show_output_context_menu)

        # 创建按钮
        self.convert_btn = QPushButton("驼峰转换")
        self.convert_btn.clicked.connect(self.convert_name)

        self.case_btn = QPushButton("大小写转换")
        self.case_btn.clicked.connect(self.toggle_case)

        self.pascal_btn = QPushButton("帕斯卡命名法")
        self.pascal_btn.clicked.connect(self.convert_to_pascal)

        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # 设置按钮间距

        # 添加按钮到布局
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.case_btn)
        button_layout.addWidget(self.pascal_btn)

        # 确保布局有足够空间显示所有按钮
        button_layout.addStretch(1)

        # 创建主布局并添加所有部件
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(QLabel("输入文本:"))
        main_layout.addWidget(self.input_text)
        main_layout.addWidget(QLabel("转换结果:"))
        main_layout.addWidget(self.output_area)

        # 设置主布局
        self.setLayout(main_layout)

    def show_input_context_menu(self, position):
        """显示输入框的右键菜单"""
        TextContextMenu.show_context_menu(self.input_text, position)

    def show_output_context_menu(self, position):
        """显示输出框的右键菜单"""
        TextContextMenu.show_context_menu(self.output_area, position)
        
    def keyPressEvent(self, event):
        """处理键盘事件"""
        # 检查是否按下了Ctrl+F
        if event.matches(QKeySequence.Find):
            # 为主文本框显示查找对话框
            self.find_manager.show_find_dialog(self.input_text)
            return
            
        super().keyPressEvent(event)

    def process(self, text: str) -> tuple:
        '''自动检测并转换命名格式'''
        is_snake = '_' in text and text.islower()
        is_camel = not is_snake and any(c.isupper() for c in text[1:])

        if is_snake:
            result = (self._to_camel(text), '下划线 → 驼峰')
            logger.info(f'转换下划线命名: "{text}" → "{result[0]}"')
            return result
        elif is_camel:
            result = (self._to_snake(text), '驼峰 → 下划线')
            logger.info(f'转换驼峰命名: "{text}" → "{result[0]}"')
            return result
        logger.debug('未检测到需要转换的命名格式: %s', text)
        return (text, '无需转换')

    def _to_camel(self, text: str) -> str:
        '''user_name → userName'''
        return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), text.lower())

    def _to_snake(self, text: str) -> str:
        '''userName → user_name'''
        text = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text).lower()

    def _to_pascal(self, text: str) -> str:
        '''将文本转换为帕斯卡命名法 (PascalCase)'''
        # 移除多余的空白字符并按行分割
        lines = text.strip().split('\n')
        pascal_results = []
        
        for line in lines:
            # 移除行内多余的空白字符，按非字母数字字符分割
            words = re.findall(r'[a-zA-Z0-9]+', line)
            if words:
                # 将每个单词首字母大写并连接
                pascal_case = ''.join(word.capitalize() for word in words)
                pascal_results.append(pascal_case)
        
        return '\n'.join(pascal_results)

    def validate_input(self, text: str) -> bool:
        return bool(text.strip())

    def get_errors(self) -> list:
        return []

    def format_content(self):
        """
        修复：使用正确的属性名 self.input_text 而不是 self.input_area
        """
        try:
            input_text = self.input_text.toPlainText()  # 修复：使用 input_text
            result, msg = self.process(input_text)
            self.output_area.setPlainText(result)  # 保持 output_area 不变
            logger.info(f'格式化成功: {msg}')
        except Exception as e:
            logger.error(f'格式化失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')

    def toggle_case(self):
        """切换文本大小写"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        # 判断当前文本主要大小写状态
        has_lower = any(c.islower() for c in input_text)
        has_upper = any(c.isupper() for c in input_text)

        if has_lower and has_upper:
            # 混合大小写时转为小写
            result = input_text.lower()
        elif has_lower:
            # 全小写转为大写
            result = input_text.upper()
        else:
            # 全大写转为小写
            result = input_text.lower()

        self.input_text.setPlainText(result)

    def convert_name(self):
        """转换变量名格式"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        try:
            result, msg = self.process(input_text)
            self.output_area.setPlainText(result)
            logger.info(f'转换成功: {msg}')
        except Exception as e:
            logger.error(f'转换失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')

    def convert_to_pascal(self):
        """将输入文本转换为帕斯卡命名法"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        try:
            result = self._to_pascal(input_text)
            self.output_area.setPlainText(result)
            logger.info('帕斯卡命名转换成功')
        except Exception as e:
            logger.error(f'帕斯卡命名转换失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')