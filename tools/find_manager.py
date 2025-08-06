# tools/find_manager.py
"""
统一的查找功能管理类
"""

from PyQt5.QtGui import QTextCursor, QTextDocument, QBrush, QColor
from PyQt5.QtWidgets import QTextEdit, QMessageBox

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
            # 检查是否有选中的文本，如果有，更新默认查找文本
            selected_text = text_edit.textCursor().selectedText()
            if selected_text:
                self.find_dialog.set_find_text(selected_text)
            self.find_dialog.show()
            self.find_dialog.raise_()
            self.find_dialog.activateWindow()
            return
            
        # 否则创建新的对话框
        self.current_text_edit = text_edit
        self.find_dialog = FindDialog(text_edit.window())
        self.find_dialog.find_signal.connect(self.perform_find)
        self.find_dialog.replace_signal.connect(self.perform_replace)
        self.find_dialog.replace_all_signal.connect(self.perform_replace_all)
        
        # 如果文本框中有选中的文本，将其作为默认查找文本
        selected_text = text_edit.textCursor().selectedText()
        if selected_text:
            self.find_dialog.set_find_text(selected_text)
            
        self.find_dialog.show()
        
    def perform_find(self, text, case_sensitive, backward, mode):
        """执行查找操作"""
        if not self.current_text_edit or not self.find_dialog:
            return
            
        text_edit = self.current_text_edit
        cursor = text_edit.textCursor()
        original_cursor = cursor
        
        # 设置查找选项
        flags = QTextDocument.FindFlags()
        if case_sensitive:
            flags |= QTextDocument.FindCaseSensitively
        if backward:
            flags |= QTextDocument.FindBackward
        
        # 处理不同查找模式
        search_text = text
        found = False
        
        if mode == 'extended':
            # 处理扩展模式的特殊字符
            # 替换斜杠为反斜杠，确保正确解析转义序列
            search_text = search_text.replace('/', '\\')
            search_text = bytes(search_text, "utf-8").decode("unicode_escape")
        elif mode == 'regex':
            # 正则表达式模式
            from PyQt5.QtCore import QRegExp
            regex = QRegExp(search_text)
            if not case_sensitive:
                regex.setCaseSensitivity(False)
            found = text_edit.document().find(regex, cursor)
            if found.isNull():
                # 没找到，从头/尾开始查找
                cursor.movePosition(QTextCursor.Start if not backward else QTextCursor.End)
                found = text_edit.document().find(regex, cursor)
                if found.isNull():
                    self.find_dialog.show_not_found_message(text)
                    return
            text_edit.setTextCursor(found)
            self.highlight_found_text(text_edit)
            return
        
        # 普通查找模式
        found = text_edit.find(search_text, flags)
        
        if not found:
            # 如果没找到，从头开始查找（或从末尾开始，如果向后查找）
            cursor.movePosition(QTextCursor.Start if not backward else QTextCursor.End)
            text_edit.setTextCursor(cursor)
            found = text_edit.find(search_text, flags)
            
            if not found:
                # 恢复原始光标位置
                text_edit.setTextCursor(original_cursor)
                self.find_dialog.show_not_found_message(text)
            else:
                # 找到但已循环
                self.highlight_found_text(text_edit)
        else:
            # 找到了
            self.highlight_found_text(text_edit)
            
    def perform_replace(self, text, replace_text, case_sensitive, backward, mode):
        """执行替换操作"""
        # 先查找
        self.perform_find(text, case_sensitive, backward, mode)
        
        # 检查是否找到
        cursor = self.current_text_edit.textCursor()
        if not cursor.hasSelection():
            return
        
        # 执行替换
        cursor.insertText(replace_text)
        self.current_text_edit.setTextCursor(cursor)
        
        # 继续查找下一个
        self.perform_find(text, case_sensitive, backward, mode)
        
    def perform_replace_all(self, text, replace_text, case_sensitive, mode):
        """执行全部替换操作"""
        if not self.current_text_edit or not text:
            return
        
        text_edit = self.current_text_edit
        
        # 获取文本光标并开始编辑块
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()
        
        # 记录起始位置
        start_pos = 0
        count = 0
        
        while True:
            # 从起始位置开始查找
            cursor.setPosition(start_pos)
            text_edit.setTextCursor(cursor)
            
            # 查找，不显示未找到提示
            found = self.perform_find_no_message(text, case_sensitive, False, mode)
            if not found:
                break
            
            # 替换
            cursor = text_edit.textCursor()
            cursor.insertText(replace_text)
            count += 1
            
            # 更新起始位置到替换后的文本之后
            start_pos = cursor.position()
        
        # 结束编辑块
        cursor.endEditBlock()
        
        # 显示替换结果
        QMessageBox.information(text_edit.window(), "替换完成", f"共替换了 {count} 处匹配")
        
    def perform_find_no_message(self, text, case_sensitive, backward, mode):
        """执行查找操作但不显示未找到提示"""
        if not self.current_text_edit or not self.find_dialog:
            return False
            
        text_edit = self.current_text_edit
        cursor = text_edit.textCursor()
        
        # 设置查找选项
        flags = QTextDocument.FindFlags()
        if case_sensitive:
            flags |= QTextDocument.FindCaseSensitively
        if backward:
            flags |= QTextDocument.FindBackward
        
        # 处理不同查找模式
        search_text = text
        if mode == 'extended':
            # 处理扩展模式的特殊字符
            # 替换斜杠为反斜杠，确保正确解析转义序列
            search_text = search_text.replace('/', '\\')
            search_text = bytes(search_text, "utf-8").decode("unicode_escape")
        elif mode == 'regex':
            # 正则表达式模式
            from PyQt5.QtCore import QRegExp
            regex = QRegExp(search_text)
            if not case_sensitive:
                regex.setCaseSensitivity(False)
            found = text_edit.document().find(regex, cursor)
            if found.isNull():
                return False
            text_edit.setTextCursor(found)
            self.highlight_found_text(text_edit)
            return True
        
        # 普通查找模式
        found = text_edit.find(search_text, flags)
        
        if not found:
            return False
        else:
            # 找到了
            self.highlight_found_text(text_edit)
            return True
        
    def highlight_found_text(self, text_edit):
        """高亮显示找到的文本为淡黄色"""
        cursor = text_edit.textCursor()
        if cursor.hasSelection():
            # 创建额外选择对象
            selection = QTextEdit.ExtraSelection()
            
            # 设置选择范围
            selection.cursor = cursor
            
            # 设置淡黄色背景
            selection.format.setBackground(QBrush(QColor(255, 220, 50)))  # 明亮的淡黄色
            
            # 应用额外选择
            text_edit.setExtraSelections([selection])
            
    def close_find_dialog(self):
        """关闭查找对话框"""
        if self.find_dialog:
            self.find_dialog.close()
            self.find_dialog = None
            self.current_text_edit = None