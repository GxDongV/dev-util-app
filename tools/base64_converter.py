import logging
import base64
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from .base_tool import BaseTool
from .text_context_menu import TextContextMenu
from .find_manager import FindManager

logger = logging.getLogger(__name__)

class Base64Converter(BaseTool):
    def __init__(self):
        super().__init__('Base64加解码')
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
        self.encode_btn = QPushButton("转为base64")
        self.encode_btn.clicked.connect(self.encode)
        
        self.decode_btn = QPushButton("解码")
        self.decode_btn.clicked.connect(self.decode)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addWidget(self.encode_btn)
        button_layout.addWidget(self.decode_btn)
        button_layout.addStretch(1)
        
        # 创建主布局并添加所有部件
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(QLabel("输入内容:"))
        main_layout.addWidget(self.input_text)
        main_layout.addWidget(QLabel("处理结果:"))
        main_layout.addWidget(self.output_area)
        
        # 设置主布局
        self.setLayout(main_layout)

    def show_input_context_menu(self, position):
        """显示输入框的右键菜单"""
        TextContextMenu.show_context_menu(self.input_text, position, self.find_manager)

    def show_output_context_menu(self, position):
        """显示输出框的右键菜单"""
        TextContextMenu.show_context_menu(self.output_area, position, self.find_manager)
        
    def keyPressEvent(self, event):
        """处理键盘事件"""
        # 检查是否按下了Ctrl+F
        if event.matches(QKeySequence.Find):
            # 为主文本框显示查找对话框
            self.find_manager.show_find_dialog(self.input_text)
            return
            
        super().keyPressEvent(event)

    def encode(self):
        """将文本编码为Base64"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        try:
            # 转换为字节并编码
            encoded_bytes = base64.b64encode(input_text.encode('utf-8'))
            result = encoded_bytes.decode('utf-8')
            self.output_area.setPlainText(result)
            logger.info('Base64编码成功')
        except Exception as e:
            logger.error(f'Base64编码失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')

    def decode(self):
        """将Base64文本解码"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        try:
            # 解码Base64并转换为文本
            decoded_bytes = base64.b64decode(input_text.encode('utf-8'))
            result = decoded_bytes.decode('utf-8')
            self.output_area.setPlainText(result)
            logger.info('Base64解码成功')
        except Exception as e:
            logger.error(f'Base64解码失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')
    
    def format_content(self):
        """实现抽象方法，这里调用编码功能作为默认格式化操作"""
        self.encode()
    
    def process(self, text: str):
        """实现BaseTool的抽象方法"""
        try:
            # 默认执行Base64编码
            encoded_bytes = base64.b64encode(text.encode('utf-8'))
            return encoded_bytes.decode('utf-8')
        except Exception as e:
            return f"处理出错: {str(e)}"