# tools/find_dialog.py
"""
通用查找替换对话框类
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QCheckBox, QGroupBox, 
                             QMessageBox, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, pyqtSignal


class FindDialog(QDialog):
    """通用查找替换对话框"""
    
    # 查找信号，参数为查找文本、是否区分大小写、是否向后查找、查找模式
    find_signal = pyqtSignal(str, bool, bool, str)
    # 替换信号，参数为查找文本、替换文本、是否区分大小写、是否向后查找、查找模式
    replace_signal = pyqtSignal(str, str, bool, bool, str)
    # 全部替换信号，参数为查找文本、替换文本、是否区分大小写、查找模式
    replace_all_signal = pyqtSignal(str, str, bool, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查找")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.resize(400, 150)
        
        self.last_text = ""
        self.last_case_sensitive = False
        self.find_mode = "normal"  # 默认普通查找模式
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout()
        
        # 查找文本行
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("查找内容:"))
        self.find_text_edit = QLineEdit()
        self.find_text_edit.textChanged.connect(self.on_text_changed)
        text_layout.addWidget(self.find_text_edit)
        layout.addLayout(text_layout)
        
        # 替换文本行
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("替换为:"))
        self.replace_text_edit = QLineEdit()
        replace_layout.addWidget(self.replace_text_edit)
        layout.addLayout(replace_layout)
        
        # 选项组
        options_group = QGroupBox("选项")
        options_layout = QVBoxLayout()
        
        self.case_sensitive_checkbox = QCheckBox("区分大小写")
        options_layout.addWidget(self.case_sensitive_checkbox)
        
        self.backward_checkbox = QCheckBox("向后查找")
        options_layout.addWidget(self.backward_checkbox)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 模式选择组
        mode_group = QGroupBox("查找模式")
        mode_layout = QVBoxLayout()
        
        self.mode_group = QButtonGroup(self)
        
        self.normal_mode_radio = QRadioButton("普通查找")
        self.normal_mode_radio.setChecked(True)
        self.normal_mode_radio.toggled.connect(lambda: self.set_mode("normal"))
        self.mode_group.addButton(self.normal_mode_radio)
        mode_layout.addWidget(self.normal_mode_radio)
        
        self.extended_mode_radio = QRadioButton("扩展 (\\n, \\r, \\t, \\0, \\x...)")
        self.extended_mode_radio.toggled.connect(lambda: self.set_mode("extended"))
        self.mode_group.addButton(self.extended_mode_radio)
        mode_layout.addWidget(self.extended_mode_radio)
        
        self.regex_mode_radio = QRadioButton("正则表达式")
        self.regex_mode_radio.toggled.connect(lambda: self.set_mode("regex"))
        self.mode_group.addButton(self.regex_mode_radio)
        mode_layout.addWidget(self.regex_mode_radio)
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.find_prev_button = QPushButton("查找上一个")
        self.find_prev_button.clicked.connect(self.find_previous)
        self.find_prev_button.setEnabled(False)
        button_layout.addWidget(self.find_prev_button)
        
        self.find_next_button = QPushButton("查找下一个")
        self.find_next_button.clicked.connect(self.find_next)
        self.find_next_button.setEnabled(False)
        button_layout.addWidget(self.find_next_button)
        
        self.replace_button = QPushButton("替换")
        self.replace_button.clicked.connect(self.replace)
        self.replace_button.setEnabled(False)
        button_layout.addWidget(self.replace_button)
        
        self.replace_all_button = QPushButton("全部替换")
        self.replace_all_button.clicked.connect(self.replace_all)
        self.replace_all_button.setEnabled(False)
        button_layout.addWidget(self.replace_all_button)
        
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 连接信号
        self.find_text_edit.returnPressed.connect(self.find_next)
        
    def set_mode(self, mode):
        """设置查找模式"""
        self.find_mode = mode
        
    def on_text_changed(self, text):
        """当查找文本改变时"""
        has_text = len(text.strip()) > 0
        self.find_next_button.setEnabled(has_text)
        self.find_prev_button.setEnabled(has_text)
        self.replace_button.setEnabled(has_text)
        self.replace_all_button.setEnabled(has_text)
        
    def find_next(self):
        """查找下一个"""
        text = self.find_text_edit.text()
        if not text.strip():
            return
            
        case_sensitive = self.case_sensitive_checkbox.isChecked()
        backward = False  # 向前查找
        
        self.find_signal.emit(text, case_sensitive, backward, self.find_mode)
        self.last_text = text
        self.last_case_sensitive = case_sensitive
        
    def find_previous(self):
        """查找上一个"""
        text = self.find_text_edit.text()
        if not text.strip():
            return
            
        case_sensitive = self.case_sensitive_checkbox.isChecked()
        backward = True  # 向后查找
        
        self.find_signal.emit(text, case_sensitive, backward, self.find_mode)
        self.last_text = text
        self.last_case_sensitive = case_sensitive
        
    def show_not_found_message(self, text):
        """显示未找到文本的消息"""
        # QMessageBox.information(self, "查找", f"未找到 '{text}'")
        
    def replace(self):
        """替换当前匹配项"""
        text = self.find_text_edit.text()
        replace_text = self.replace_text_edit.text()
        if not text.strip():
            return
            
        case_sensitive = self.case_sensitive_checkbox.isChecked()
        backward = self.backward_checkbox.isChecked()
        
        self.replace_signal.emit(text, replace_text, case_sensitive, backward, self.find_mode)
        self.last_text = text
        self.last_case_sensitive = case_sensitive
        
    def replace_all(self):
        """替换所有匹配项"""
        text = self.find_text_edit.text()
        replace_text = self.replace_text_edit.text()
        if not text.strip():
            return
            
        case_sensitive = self.case_sensitive_checkbox.isChecked()
        
        self.replace_all_signal.emit(text, replace_text, case_sensitive, self.find_mode)
        self.last_text = text
        self.last_case_sensitive = case_sensitive
        
    def get_find_options(self):
        """获取当前查找选项"""
        return {
            'text': self.find_text_edit.text(),
            'case_sensitive': self.case_sensitive_checkbox.isChecked(),
            'backward': self.backward_checkbox.isChecked(),
            'mode': self.find_mode
        }
        
    def set_find_text(self, text):
        """设置查找文本"""
        self.find_text_edit.setText(text)
        self.find_text_edit.selectAll()