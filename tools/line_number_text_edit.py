#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
带行号显示的QTextEdit组件
仅支持行号显示功能
"""

import sys

from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtGui import QPainter, QFont, QColor, QTextFormat
from PyQt5.QtWidgets import QTextEdit, QApplication, QWidget


class LineNumberArea(QWidget):
    """行号区域"""
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        # 设置为直角边框
        self.setStyleSheet("QWidget { border-radius: 0px; border-right: 1px solid #ccc; }")

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class LineNumberTextEdit(QTextEdit):
    """带行号显示的文本编辑器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置字体
        self.setFont(QFont("Microsoft YaHei", 10, QFont.Normal))
        # 不自动换行
        self.setLineWrapMode(QTextEdit.NoWrap)
        # 设置为直角边框
        self.setStyleSheet("QTextEdit { border-radius: 0px; }")
        # 创建行号区域
        self.line_number_area = LineNumberArea(self)

        # 添加主体颜色属性
        self.is_dark_theme = False

        # 连接信号
        self.document().blockCountChanged.connect(self.update_line_number_area_width)
        self.verticalScrollBar().valueChanged.connect(self.line_number_area.update)
        self.textChanged.connect(self.line_number_area.update)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.cursorPositionChanged.connect(self.line_number_area.update)

        # 初始化行号区域宽度
        self.update_line_number_area_width()
        self.highlight_current_line()

    def set_dark_theme(self, is_dark):
        """设置主体颜色主题"""
        self.is_dark_theme = is_dark
        # 更新行号区域和当前行高亮
        self.line_number_area.update()
        self.highlight_current_line()

    def line_number_area_width(self):
        """计算行号区域宽度"""
        block_count = self.document().blockCount()
        max_value = max(1, block_count)
        d_count = len(str(max_value))
        _width = self.fontMetrics().width('9') * d_count + 5
        return _width

    def update_line_number_area_width(self):
        """更新行号区域宽度"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def resizeEvent(self, event):
        """重写resize事件"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(),
                                              self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        """高亮当前行"""
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            # 根据主题设置高亮颜色
            if self.is_dark_theme:
                line_color = QColor(84, 104, 122)
            else:
                line_color = QColor(230, 230, 230)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        """行号区域绘制事件"""
        painter = QPainter(self.line_number_area)
        # 根据主题设置背景颜色
        if self.is_dark_theme:
            painter.fillRect(event.rect(), QColor(84, 104, 122))
        else:
            painter.fillRect(event.rect(), QColor(230, 230, 230))

        # 获取首个可见文本块
        first_visible_block_number = self.cursorForPosition(QPoint(0, 1)).blockNumber()
        # 从首个文本块开始处理
        blockNumber = first_visible_block_number
        block = self.document().findBlockByNumber(blockNumber)
        top = self.viewport().geometry().top()

        if blockNumber == 0:
            additional_margin = int(self.document().documentMargin() - 1 - self.verticalScrollBar().sliderPosition())
        else:
            prev_block = self.document().findBlockByNumber(blockNumber - 1)
            additional_margin = int(self.document().documentLayout().blockBoundingRect(
                prev_block).bottom()) - self.verticalScrollBar().sliderPosition()
        top += additional_margin
        bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())

        last_block_number = self.cursorForPosition(QPoint(0, self.height() - 1)).blockNumber()
        height = self.fontMetrics().height()
        current_line = self.textCursor().blockNumber()

        while block.isValid() and (top <= event.rect().bottom()) and blockNumber <= last_block_number:
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                # 如果是当前行，改变颜色
                if blockNumber == current_line:
                    painter.setPen(Qt.blue)  # 当前行号颜色为蓝色
                else:
                    # 根据主题设置行号颜色
                    if self.is_dark_theme:
                        painter.setPen(Qt.white)
                    else:
                        painter.setPen(Qt.black)
                painter.drawText(0, top, self.line_number_area.width(), height, Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
            blockNumber += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    codeEditor = LineNumberTextEdit()
    codeEditor.setGeometry(100, 100, 800, 600)
    codeEditor.show()
    sys.exit(app.exec_())