# tools/text_context_menu.py
"""
统一处理QTextEdit的中文右键菜单
"""

from PyQt5.QtWidgets import QMenu, QAction


class TextContextMenu:
    """文本框右键菜单处理器"""
    
    @staticmethod
    def show_context_menu(text_edit, position, find_manager=None):
        """显示文本编辑器的自定义中文右键菜单"""
        menu = QMenu()
        
        # 添加标准文本编辑操作
        undo_action = QAction("撤销", text_edit)
        undo_action.setEnabled(text_edit.document().isUndoAvailable())
        undo_action.triggered.connect(text_edit.undo)
        menu.addAction(undo_action)
        
        redo_action = QAction("重做", text_edit)
        redo_action.setEnabled(text_edit.document().isRedoAvailable())
        redo_action.triggered.connect(text_edit.redo)
        menu.addAction(redo_action)
        
        menu.addSeparator()
        
        cut_action = QAction("剪切", text_edit)
        cut_action.setEnabled(text_edit.textCursor().hasSelection())
        cut_action.triggered.connect(text_edit.cut)
        menu.addAction(cut_action)
        
        copy_action = QAction("复制", text_edit)
        copy_action.setEnabled(text_edit.textCursor().hasSelection())
        copy_action.triggered.connect(text_edit.copy)
        menu.addAction(copy_action)
        
        paste_action = QAction("粘贴", text_edit)
        paste_action.setEnabled(text_edit.canPaste())
        paste_action.triggered.connect(text_edit.paste)
        menu.addAction(paste_action)
        
        delete_action = QAction("删除", text_edit)
        delete_action.setEnabled(text_edit.textCursor().hasSelection())
        delete_action.triggered.connect(lambda: text_edit.textCursor().removeSelectedText())
        menu.addAction(delete_action)
        
        menu.addSeparator()
        
        select_all_action = QAction("全选", text_edit)
        select_all_action.triggered.connect(text_edit.selectAll)
        menu.addAction(select_all_action)
        
        # 如果提供了查找管理器，则添加查找功能
        if find_manager:
            menu.addSeparator()
            find_action = QAction("查找", text_edit)
            find_action.triggered.connect(lambda: find_manager.show_find_dialog(text_edit))
            menu.addAction(find_action)
        
        menu.exec_(text_edit.mapToGlobal(position))