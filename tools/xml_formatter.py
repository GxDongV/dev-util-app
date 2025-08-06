# tools/xml_formatter.py
import json
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QKeySequence
from PyQt5.QtWidgets import (QVBoxLayout, QPushButton, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QSplitter, QMenu,
                             QAction, QApplication, QMessageBox)

from .base_tool import BaseTool
from .find_manager import FindManager
from .line_number_text_edit import LineNumberTextEdit
from .text_context_menu import TextContextMenu


class XmlFormatter(BaseTool):
    def __init__(self):
        super().__init__("XML编辑器")
        self.find_manager = FindManager()
        self.original_input = None  # 保存原始输入
        self.is_converted_to_json = False  # 标记是否已转换为JSON

    def init_ui(self):
        """
        重写init_ui方法，创建独立的UI布局
        """
        layout = QVBoxLayout()
        
        # 创建水平布局用于放置按钮在左上角
        button_layout = QHBoxLayout()
        self.convert_btn = QPushButton("格式化XML")
        self.convert_btn.clicked.connect(self.format_content)
        
        # 添加转为JSON按钮
        self.to_json_btn = QPushButton("转为JSON")
        self.to_json_btn.clicked.connect(self.convert_to_json)
        
        # 添加展开和合并按钮
        self.expand_btn = QPushButton("全部展开")
        self.expand_btn.clicked.connect(self.expand_all)
        self.collapse_btn = QPushButton("全部合并")
        self.collapse_btn.clicked.connect(self.collapse_all)
        
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.to_json_btn)
        button_layout.addWidget(self.expand_btn)
        button_layout.addWidget(self.collapse_btn)
        button_layout.addStretch()  # 添加弹性空间，使按钮保持在左侧
        
        # 创建分割器用于分开展示文本和树形视图
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧文本编辑区域
        self.input_area = LineNumberTextEdit()
        self.input_area.setPlaceholderText("请输入或粘贴XML内容，然后点击上方按钮进行格式化...")
        # 启用右键菜单
        self.input_area.setContextMenuPolicy(Qt.CustomContextMenu)
        self.input_area.customContextMenuRequested.connect(self.show_text_context_menu)
        
        # 右侧树形视图区域
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Element", "Attributes", "Text"])
        self.tree_widget.setAlternatingRowColors(True)
        # 启用右键菜单
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
        
        splitter.addWidget(self.input_area)
        splitter.addWidget(self.tree_widget)
        
        layout.addLayout(button_layout)
        layout.addWidget(splitter)

        self.setLayout(layout)

    def format_content(self):
        """
        实现XML格式化逻辑
        """
        input_text = self.input_area.toPlainText()
        if not input_text.strip():
            QMessageBox.warning(self, "输入错误", "请输入XML内容")
            return

        try:
            # 解析并格式化XML
            import xml.dom.minidom
            dom = xml.dom.minidom.parseString(input_text)
            formatted_xml = dom.toprettyxml(indent="    ")
            # 移除XML声明前的空行
            formatted_xml = '\n'.join(line for line in formatted_xml.split('\n') if line.strip())
            self.input_area.setPlainText(formatted_xml)
            
            # 更新树形视图
            self.update_tree_view(input_text)
        except Exception as e:
            QMessageBox.warning(self, "格式错误", f"请输入正确的XML格式\n错误信息: {str(e)}")

    def convert_to_json(self):
        """
        将XML转换为JSON格式，或恢复原始XML输入
        """
        # 如果已经转换为JSON，则恢复原始输入
        if self.is_converted_to_json and self.original_input:
            self.input_area.setPlainText(self.original_input)
            self.update_tree_view(self.original_input)
            self.to_json_btn.setText("转为JSON")
            self.is_converted_to_json = False
            return

        input_text = self.input_area.toPlainText()
        if not input_text.strip():
            QMessageBox.warning(self, "输入错误", "请输入XML内容")
            return

        # 保存原始输入
        self.original_input = input_text

        try:
            # 解析XML
            root = ET.fromstring(input_text)
            
            # 转换为字典
            data = self._xml_to_dict(root)
            
            # 转换为JSON
            json_str = json.dumps(data, indent=4, ensure_ascii=False)
            
            # 显示结果
            self.input_area.setPlainText(json_str)
            
            # 更新按钮文本
            self.to_json_btn.setText("恢复原始XML")
            self.is_converted_to_json = True
            
            # 更新树形视图，添加提示信息
            self.update_tree_view('<root><message>已转换为JSON格式，请在左侧查看</message></root>')
        except ET.ParseError as e:
            QMessageBox.warning(self, "格式错误", f"请输入正确的XML格式\n错误信息: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "处理错误", f"处理出错: {str(e)}")

    def _xml_to_dict(self, element):
        """
        递归将XML元素转换为字典
        """
        # 获取元素的属性
        attrs = element.attrib
        
        # 获取元素的文本内容
        text = element.text.strip() if element.text else ""
        
        # 获取子元素
        children = list(element)
        
        # 构建结果字典
        result = {}
        
        # 添加属性
        if attrs:
            result["@attributes"] = attrs
            
        # 处理子元素
        if children:
            child_dict = {}
            for child in children:
                child_data = self._xml_to_dict(child)
                if child.tag in child_dict:
                    # 如果标签已存在，转换为列表
                    if not isinstance(child_dict[child.tag], list):
                        child_dict[child.tag] = [child_dict[child.tag]]
                    child_dict[child.tag].append(child_data)
                else:
                    child_dict[child.tag] = child_data
            
            # 合并子元素到结果中
            result.update(child_dict)
            
            # 如果有文本内容，添加到特殊键中
            if text:
                result["#text"] = text
        else:
            # 没有子元素，直接返回文本或空字典
            if text:
                if attrs:
                    result["#text"] = text
                else:
                    return text
            elif not attrs:
                return ""
        
        return result

    def update_tree_view(self, xml_text):
        """
        更新树形视图显示XML结构
        """
        self.tree_widget.clear()
        try:
            # 如果传入的是字符串，则解析为XML元素
            if isinstance(xml_text, str):
                root = ET.fromstring(xml_text)
            else:
                # 如果传入的是XML元素，则直接使用
                root = xml_text
            self.add_tree_items(self.tree_widget, root)
            self.tree_widget.expandAll()
        except ET.ParseError as e:
            # 如果解析失败，在树形视图中显示错误
            error_item = QTreeWidgetItem(["解析错误", "", str(e)])
            self.tree_widget.addTopLevelItem(error_item)

    def add_tree_items(self, parent, element):
        """
        递归添加树形节点
        """
        # 获取元素标签名
        tag = element.tag
        
        # 获取元素属性
        attrs = ", ".join([f"{k}={v}" for k, v in element.attrib.items()]) if element.attrib else ""
        
        # 获取元素文本内容
        text = element.text.strip() if element.text else ""
        
        # 创建树节点
        item = QTreeWidgetItem([tag, attrs, text])
        
        # 添加到父节点
        if isinstance(parent, QTreeWidget):
            parent.addTopLevelItem(item)
        else:
            parent.addChild(item)
        
        # 递归添加子元素
        for child in element:
            self.add_tree_items(item, child)

    def expand_all(self):
        """
        展开所有节点
        """
        self.tree_widget.expandAll()

    def collapse_all(self):
        """
        合并所有节点
        """
        self.tree_widget.collapseAll()
        
    def show_text_context_menu(self, position):
        """显示文本编辑区域的右键菜单"""
        TextContextMenu.show_context_menu(self.input_area, position, self.find_manager)
        
    def keyPressEvent(self, event):
        """处理键盘事件"""
        # 检查是否按下了Ctrl+F
        if event.matches(QKeySequence.Find):
            # 为主文本框显示查找对话框
            self.find_manager.show_find_dialog(self.input_area)
            return
            
        super().keyPressEvent(event)
        
    def show_context_menu(self, position):
        """
        显示右键菜单
        """
        # 获取点击的项
        item = self.tree_widget.itemAt(position)
        if not item:
            return
            
        # 创建菜单
        menu = QMenu()
        
        # 添加复制元素名的选项
        copy_element_action = QAction("复制 Element", self)
        copy_element_action.triggered.connect(lambda: self.copy_to_clipboard(item.text(0)))
        menu.addAction(copy_element_action)
        
        # 添加复制属性的选项
        copy_attrs_action = QAction("复制 Attributes", self)
        copy_attrs_action.triggered.connect(lambda: self.copy_to_clipboard(item.text(1)))
        menu.addAction(copy_attrs_action)
        
        # 添加复制文本的选项
        copy_text_action = QAction("复制 Text", self)
        copy_text_action.triggered.connect(lambda: self.copy_to_clipboard(item.text(2)))
        menu.addAction(copy_text_action)
        
        # 添加复制全部信息的选项
        copy_all_action = QAction("复制全部信息", self)
        copy_all_action.triggered.connect(lambda: self.copy_to_clipboard(
            f"Element: {item.text(0)}\nAttributes: {item.text(1)}\nText: {item.text(2)}"))
        menu.addAction(copy_all_action)
        
        # 显示菜单
        menu.exec_(QCursor.pos())

    def copy_to_clipboard(self, text):
        """
        复制文本到剪贴板
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def process(self, text: str):
        """
        实现BaseTool的抽象方法
        """
        try:
            # 这里可以实现更复杂的XML处理逻辑
            import xml.dom.minidom
            dom = xml.dom.minidom.parseString(text)
            formatted_xml = dom.toprettyxml(indent="    ")
            # 移除XML声明前的空行
            formatted_xml = '\n'.join(line for line in formatted_xml.split('\n') if line.strip())
            return formatted_xml
        except Exception as e:
            return f"处理出错: {str(e)}"