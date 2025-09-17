"""
集成查找功能、行号显示和文件操作的文本编辑器
"""

from PyQt5.QtWidgets import (QWidget, QComboBox, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt
from .line_number_text_edit import LineNumberTextEdit
from .find_manager import FindManager
import os


class TextEditorWithFind(LineNumberTextEdit):
    """集成查找功能、行号显示和文件操作的文本编辑器"""
    
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.find_manager = FindManager()
        self.file_path = None  # 初始化文件路径属性
        self.init_ui()
        
    def init_ui(self):
        """初始化UI元素"""
        # 创建顶部工具栏
        self.toolbar_layout = QHBoxLayout()
        
        # 编码选择下拉框
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["utf-8", "gbk", "gb2312", "utf-16"])
        self.encoding_combo.setCurrentText("utf-8")
        self.encoding_combo.setToolTip("选择文件编码")
        self.encoding_combo.currentTextChanged.connect(self.on_encoding_changed)
        self.toolbar_layout.addWidget(self.encoding_combo)
        
        # 添加伸展项，将控件推到左侧
        self.toolbar_layout.addStretch()
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.toolbar_layout)
        main_layout.addWidget(self)
        
        # 创建容器窗口
        self.container = QWidget()
        self.container.setLayout(main_layout)
        
    def show_find_dialog(self):
        """显示查找对话框"""
        self.find_manager.show_find_dialog(self)
    
    def on_encoding_changed(self, new_encoding):
        """当编码选择变化时触发"""
        try:
            # 获取当前文本
            current_text = self.toPlainText()
            
            # 尝试转换编码
            if current_text:
                # 先将文本编码为字节(使用utf-8作为中间编码)
                text_bytes = current_text.encode('utf-8')
                # 再解码为新编码
                new_text = text_bytes.decode(new_encoding)
                # 更新文本
                self.setPlainText(new_text)
        except Exception as e:
            print(f"编码转换错误: {e}")