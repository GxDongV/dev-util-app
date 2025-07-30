# tools/text_statistics.py

import logging
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QSizePolicy
import re
from .base_tool import BaseTool
from .text_context_menu import TextContextMenu
from .find_manager import FindManager

logger = logging.getLogger(__name__)


class TextStatistics(BaseTool):
    def __init__(self):
        super().__init__('文本统计工具')
        self.find_manager = FindManager()
        
        # 创建输入文本框
        self.input_text = QTextEdit()
        self.input_text.textChanged.connect(self.update_statistics)
        self.input_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.input_text.customContextMenuRequested.connect(self.show_input_context_menu)
        
        # 创建统计结果显示区域
        self.stats_frame = QFrame()
        self.stats_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        # 设置框架的最大宽度，使其只占原来的一半
        self.stats_frame.setMaximumWidth(300)
        stats_layout = QGridLayout(self.stats_frame)
        
        # 设置列伸缩属性，让第二列（统计数值列）占据更多空间
        stats_layout.setColumnStretch(0, 1)  # 标签列
        stats_layout.setColumnStretch(1, 1)  # 数值列
        
        # 初始化统计标签和显示框
        # 使用QLineEdit并设置为只读，这样用户可以选中和复制内容
        self.total_chars_label = QLineEdit("0")
        self.total_chars_label.setReadOnly(True)
        self.total_chars_label.setAlignment(Qt.AlignRight)
        self.total_words_label = QLineEdit("0")
        self.total_words_label.setReadOnly(True)
        self.total_words_label.setAlignment(Qt.AlignRight)
        self.chinese_chars_label = QLineEdit("0")
        self.chinese_chars_label.setReadOnly(True)
        self.chinese_chars_label.setAlignment(Qt.AlignRight)
        self.chinese_punctuation_label = QLineEdit("0")
        self.chinese_punctuation_label.setReadOnly(True)
        self.chinese_punctuation_label.setAlignment(Qt.AlignRight)
        self.english_letters_label = QLineEdit("0")
        self.english_letters_label.setReadOnly(True)
        self.english_letters_label.setAlignment(Qt.AlignRight)
        self.english_words_label = QLineEdit("0")
        self.english_words_label.setReadOnly(True)
        self.english_words_label.setAlignment(Qt.AlignRight)
        self.english_punctuation_label = QLineEdit("0")
        self.english_punctuation_label.setReadOnly(True)
        self.english_punctuation_label.setAlignment(Qt.AlignRight)
        self.digits_label = QLineEdit("0")
        self.digits_label.setReadOnly(True)
        self.digits_label.setAlignment(Qt.AlignRight)
        self.char_length_label = QLineEdit("0")
        self.char_length_label.setReadOnly(True)
        self.char_length_label.setAlignment(Qt.AlignRight)
        self.byte_size_label = QLineEdit("0 bytes")
        self.byte_size_label.setReadOnly(True)
        self.byte_size_label.setAlignment(Qt.AlignRight)
        
        # 添加标签到布局
        stats_layout.addWidget(QLabel("总字数:"), 0, 0)
        stats_layout.addWidget(self.total_chars_label, 0, 1)
        stats_layout.addWidget(QLabel("总字符数:"), 1, 0)
        stats_layout.addWidget(self.total_words_label, 1, 1)
        stats_layout.addWidget(QLabel("总汉字数:"), 2, 0)
        stats_layout.addWidget(self.chinese_chars_label, 2, 1)
        stats_layout.addWidget(QLabel("汉字符号:"), 3, 0)
        stats_layout.addWidget(self.chinese_punctuation_label, 3, 1)
        stats_layout.addWidget(QLabel("外文字母:"), 4, 0)
        stats_layout.addWidget(self.english_letters_label, 4, 1)
        stats_layout.addWidget(QLabel("外文单词:"), 5, 0)
        stats_layout.addWidget(self.english_words_label, 5, 1)
        stats_layout.addWidget(QLabel("外文符号:"), 6, 0)
        stats_layout.addWidget(self.english_punctuation_label, 6, 1)
        stats_layout.addWidget(QLabel("数字:"), 7, 0)
        stats_layout.addWidget(self.digits_label, 7, 1)
        stats_layout.addWidget(QLabel("字符长度:"), 8, 0)
        stats_layout.addWidget(self.char_length_label, 8, 1)
        stats_layout.addWidget(QLabel("字节大小:"), 9, 0)
        stats_layout.addWidget(self.byte_size_label, 9, 1)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("输入文本:"))
        main_layout.addWidget(self.input_text)
        main_layout.addWidget(QLabel("统计结果:"))
        main_layout.addWidget(self.stats_frame)
        
        # 设置主布局
        self.setLayout(main_layout)
        
        # 初始化统计数据
        self.update_statistics()

    def show_input_context_menu(self, position):
        """显示输入框的右键菜单"""
        TextContextMenu.show_context_menu(self.input_text, position, self.find_manager)
        
    def keyPressEvent(self, event):
        """处理键盘事件"""
        # 检查是否按下了Ctrl+F
        if event.matches(QKeySequence.Find):
            # 为主文本框显示查找对话框
            self.find_manager.show_find_dialog(self.input_text)
            return
            
        super().keyPressEvent(event)

    def count_chinese_characters(self, text):
        """统计汉字数量"""
        return len(re.findall(r'[\u4e00-\u9fff]', text))

    def count_chinese_punctuation(self, text):
        """统计汉字符号数量"""
        chinese_punctuation = r'[，。！？；：""''（）【】《》、]+'
        return len(re.findall(chinese_punctuation, text))

    def count_english_letters(self, text):
        """统计外文字母数量"""
        return len(re.findall(r'[a-zA-Z]', text))

    def count_english_words(self, text):
        """统计外文单词数量"""
        # 匹配由字母组成的单词
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        return len(words)

    def count_english_punctuation(self, text):
        """统计外文符号数量"""
        english_punctuation = r'[.,!?;:"\'()\[\]{}\-+=_`~#@%^&*<>\\/]+'
        return len(re.findall(english_punctuation, text))

    def count_digits(self, text):
        """统计数字数量"""
        return len(re.findall(r'\d', text))

    def update_statistics(self):
        """更新统计数据"""
        text = self.input_text.toPlainText()
        
        # 计算各种统计数据
        total_chars = len(text)
        total_words = len(text.split()) if text else 0
        chinese_chars = self.count_chinese_characters(text)
        chinese_punctuation = self.count_chinese_punctuation(text)
        english_letters = self.count_english_letters(text)
        english_words = self.count_english_words(text)
        english_punctuation = self.count_english_punctuation(text)
        digits = self.count_digits(text)
        char_length = len(text)
        byte_size = len(text.encode('utf-8'))
        
        # 更新标签显示
        self.total_chars_label.setText(str(total_chars))
        self.total_words_label.setText(str(total_words))
        self.chinese_chars_label.setText(str(chinese_chars))
        self.chinese_punctuation_label.setText(str(chinese_punctuation))
        self.english_letters_label.setText(str(english_letters))
        self.english_words_label.setText(str(english_words))
        self.english_punctuation_label.setText(str(english_punctuation))
        self.digits_label.setText(str(digits))
        self.char_length_label.setText(str(char_length))
        self.byte_size_label.setText(str(byte_size) + " bytes")

    def format_content(self):
        """实现抽象方法"""
        self.update_statistics()
    
    def process(self, text: str):
        """实现BaseTool的抽象方法"""
        try:
            # 返回文本统计信息的字符串表示
            total_chars = len(text)
            total_words = len(text.split()) if text else 0
            chinese_chars = self.count_chinese_characters(text)
            chinese_punctuation = self.count_chinese_punctuation(text)
            english_letters = self.count_english_letters(text)
            english_words = self.count_english_words(text)
            english_punctuation = self.count_english_punctuation(text)
            digits = self.count_digits(text)
            char_length = len(text)
            byte_size = len(text.encode('utf-8'))
            
            result = f"""总字数: {total_chars}
总字符数: {total_words}
总汉字数: {chinese_chars}
汉字符号: {chinese_punctuation}
外文字母: {english_letters}
外文单词: {english_words}
外文符号: {english_punctuation}
数字: {digits}
字符长度: {char_length}
字节大小: {byte_size} bytes"""
            return result
        except Exception as e:
            return f"处理出错: {str(e)}"