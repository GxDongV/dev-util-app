# tools/json_formatter.py
from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QWidget, QLabel, QTreeWidget, QTreeWidgetItem, QSplitter, QMenu, QAction, QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QKeySequence
from .base_tool import BaseTool
from .text_context_menu import TextContextMenu
from .find_manager import FindManager
from .line_number_text_edit import LineNumberTextEdit
import json
import xml.etree.ElementTree as ET

class JsonFormatter(BaseTool):
    def __init__(self):
        super().__init__("JSON编辑器")
        self.find_manager = FindManager()
        self.original_input = None  # 保存原始输入
        self.is_converted_to_xml = False  # 标记是否已转换为XML

    def init_ui(self):
        """
        重写init_ui方法，创建独立的UI布局
        """
        layout = QVBoxLayout()
        
        # 创建水平布局用于放置按钮在左上角
        button_layout = QHBoxLayout()
        self.convert_btn = QPushButton("格式化JSON")
        self.convert_btn.clicked.connect(self.format_content)
        
        # 添加转为XML按钮
        self.to_xml_btn = QPushButton("转为XML")
        self.to_xml_btn.clicked.connect(self.convert_to_xml)
        
        # 添加展开和合并按钮
        self.expand_btn = QPushButton("全部展开")
        self.expand_btn.clicked.connect(self.expand_all)
        self.collapse_btn = QPushButton("全部合并")
        self.collapse_btn.clicked.connect(self.collapse_all)
        
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.to_xml_btn)
        button_layout.addWidget(self.expand_btn)
        button_layout.addWidget(self.collapse_btn)
        button_layout.addStretch()  # 添加弹性空间，使按钮保持在左侧
        
        # 创建分割器用于分展开示文本和树形视图
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧文本编辑区域
        self.input_area = LineNumberTextEdit()
        self.input_area.setPlaceholderText("请输入或粘贴JSON内容，然后点击上方按钮进行格式化...")
        # 启用右键菜单
        self.input_area.setContextMenuPolicy(Qt.CustomContextMenu)
        self.input_area.customContextMenuRequested.connect(self.show_text_context_menu)
        
        # 右侧树形视图区域
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Key", "Value"])
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
        实现JSON格式化逻辑
        """
        input_text = self.input_area.toPlainText()
        if not input_text.strip():
            QMessageBox.warning(self, "输入错误", "请输入JSON内容")
            return

        try:
            # 解析并格式化JSON
            parsed_json = json.loads(input_text)
            formatted_json = json.dumps(parsed_json, indent=4, ensure_ascii=False)
            self.input_area.setPlainText(formatted_json)
            
            # 更新树形视图
            self.update_tree_view(parsed_json)
        except json.JSONDecodeError as e:
            QMessageBox.warning(self, "格式错误", f"请输入正确的JSON格式\n错误信息: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "处理错误", f"处理出错: {str(e)}")

    def convert_to_xml(self):
        """
        将JSON转换为XML格式，或恢复原始JSON输入
        """
        # 如果已经转换为XML，则恢复原始输入
        if self.is_converted_to_xml and self.original_input:
            self.input_area.setPlainText(self.original_input)
            self.update_tree_view(json.loads(self.original_input))
            self.to_xml_btn.setText("转为XML")
            self.is_converted_to_xml = False
            return

        input_text = self.input_area.toPlainText()
        if not input_text.strip():
            QMessageBox.warning(self, "输入错误", "请输入JSON内容")
            return

        # 保存原始输入
        self.original_input = input_text

        try:
            # 解析JSON
            parsed_json = json.loads(input_text)
            
            # 创建根元素
            root = ET.Element("root")
            
            # 递归转换JSON到XML
            self._dict_to_xml(parsed_json, root)
            
            # 生成XML字符串
            xml_str = ET.tostring(root, encoding='unicode')
            
            # 格式化XML
            import xml.dom.minidom
            dom = xml.dom.minidom.parseString(xml_str)
            formatted_xml = dom.toprettyxml(indent="    ")
            # 移除XML声明前的空行
            formatted_xml = '\n'.join(line for line in formatted_xml.split('\n') if line.strip())
            
            # 显示结果
            self.input_area.setPlainText(formatted_xml)
            
            # 更新按钮文本
            self.to_xml_btn.setText("恢复原始JSON")
            self.is_converted_to_xml = True
            
            # 更新树形视图
            self.update_tree_view({"message": "已转换为XML格式，请在左侧查看"})
        except json.JSONDecodeError as e:
            QMessageBox.warning(self, "格式错误", f"请输入正确的JSON格式\n错误信息: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "处理错误", f"处理出错: {str(e)}")

    def _dict_to_xml(self, data, parent):
        """
        递归将字典转换为XML元素
        """
        if isinstance(data, dict):
            for key, value in data.items():
                element = ET.SubElement(parent, key)
                self._dict_to_xml(value, element)
        elif isinstance(data, list):
            for item in data:
                element = ET.SubElement(parent, "item")
                self._dict_to_xml(item, element)
        else:
            parent.text = str(data)

    def update_tree_view(self, data):
        """
        更新树形视图显示JSON结构
        """
        self.tree_widget.clear()
        self.add_tree_items(self.tree_widget, data)
        self.tree_widget.expandAll()

    def add_tree_items(self, parent, data, key=""):
        """
        递归添加树形节点
        """
        if isinstance(data, dict):
            for k, v in data.items():
                item = QTreeWidgetItem([k, ""])
                parent.addTopLevelItem(item) if isinstance(parent, QTreeWidget) else parent.addChild(item)
                self.add_tree_items(item, v, k)
        elif isinstance(data, list):
            for i, v in enumerate(data):
                item = QTreeWidgetItem([f"[{i}]", ""])
                parent.addTopLevelItem(item) if isinstance(parent, QTreeWidget) else parent.addChild(item)
                self.add_tree_items(item, v, f"[{i}]")
        else:
            parent.setText(1, str(data))

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
        
        # 添加复制key的选项
        copy_key_action = QAction("复制 Key", self)
        copy_key_action.triggered.connect(lambda: self.copy_to_clipboard(item.text(0)))
        menu.addAction(copy_key_action)
        
        # 添加复制value的选项
        copy_value_action = QAction("复制 Value", self)
        copy_value_action.triggered.connect(lambda: self.copy_to_clipboard(item.text(1)))
        menu.addAction(copy_value_action)
        
        # 添加复制key和value的选项
        copy_both_action = QAction("复制 Key 和 Value", self)
        copy_both_action.triggered.connect(lambda: self.copy_to_clipboard(f"{item.text(0)}: {item.text(1)}"))
        menu.addAction(copy_both_action)
        
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
            parsed = json.loads(text)
            return json.dumps(parsed, indent=4, ensure_ascii=False)
        except Exception as e:
            return f"处理出错: {str(e)}"