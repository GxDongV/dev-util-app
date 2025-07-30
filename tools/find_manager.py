# tools/find_manager.py
"""
统一的查找功能管理类
"""

from PyQt5.QtWidgets import QTextEdit, QMessageBox
from PyQt5.QtGui import QTextCursor, QTextDocument
from .find_dialog import FindDialog


class FindManager:
    """查找功能管理器"""
    
    def __init__(self):
        self.find_dialog = None
        self.current_text_edit = None
        
    def show_find_dialog(self, text_edit):
        """显示查找对话框"""
        # 如果已经有对话框且关联的是同一个文本框，则显示它
        if self.find_dialog and self.current_text_edit == text_edit:
            self.find_dialog.show()
            self.find_dialog.raise_()
            self.find_dialog.activateWindow()
            return
            
        # 否则创建新的对话框
        self.current_text_edit = text_edit
        self.find_dialog = FindDialog(text_edit.window())
        self.find_dialog.find_signal.connect(self.perform_find)
        
        # 如果文本框中有选中的文本，将其作为默认查找文本
        selected_text = text_edit.textCursor().selectedText()
        if selected_text:
            self.find_dialog.set_find_text(selected_text)
            
        self.find_dialog.show()
        
    def perform_find(self, text, case_sensitive, backward):
        """执行查找操作"""
        if not self.current_text_edit or not self.find_dialog:
            return
            
        text_edit = self.current_text_edit
        cursor = text_edit.textCursor()
        
        # 设置查找选项
        flags = QTextDocument.FindFlags()
        if case_sensitive:
            flags |= QTextDocument.FindCaseSensitively
        if backward:
            flags |= QTextDocument.FindBackward
            
        # 执行查找
        found = text_edit.find(text, flags)
        
        if not found:
            # 如果没找到，从头开始查找（或从末尾开始，如果向后查找）
            cursor.movePosition(QTextCursor.Start if not backward else QTextCursor.End)
            text_edit.setTextCursor(cursor)
            found = text_edit.find(text, flags)
            
            if not found:
                self.find_dialog.show_not_found_message(text)
            else:
                # 找到但已循环
                self.highlight_found_text(text_edit)
        else:
            # 找到了
            self.highlight_found_text(text_edit)
            
    def highlight_found_text(self, text_edit):
        """高亮显示找到的文本"""
        cursor = text_edit.textCursor()
        if cursor.hasSelection():
            text_edit.setTextCursor(cursor)
            
    def close_find_dialog(self):
        """关闭查找对话框"""
        if self.find_dialog:
            self.find_dialog.close()
            self.find_dialog = None
            self.current_text_edit = None