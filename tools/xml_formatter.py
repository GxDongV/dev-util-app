# tools/xml_formatter.py
from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QSplitter, QMenu, QAction, QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from .base_tool import BaseTool
import xml.etree.ElementTree as ET


class XmlFormatter(BaseTool):
    def __init__(self):
        super().__init__("XML编辑器")

    def init_ui(self):
        """
        重写init_ui方法，创建独立的UI布局
        """
        layout = QVBoxLayout()
        
        # 创建水平布局用于放置按钮在左上角
        button_layout = QHBoxLayout()
        self.convert_btn = QPushButton("格式化XML")
        self.convert_btn.clicked.connect(self.format_content)
        
        # 添加展开和合并按钮
        self.expand_btn = QPushButton("全部展开")
        self.expand_btn.clicked.connect(self.expand_all)
        self.collapse_btn = QPushButton("全部合并")
        self.collapse_btn.clicked.connect(self.collapse_all)
        
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.expand_btn)
        button_layout.addWidget(self.collapse_btn)
        button_layout.addStretch()  # 添加弹性空间，使按钮保持在左侧
        
        # 创建分割器用于分开展示文本和树形视图
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧文本编辑区域
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("请输入或粘贴XML内容，然后点击上方按钮进行格式化...")
        
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

    def update_tree_view(self, xml_text):
        """
        更新树形视图显示XML结构
        """
        self.tree_widget.clear()
        try:
            root = ET.fromstring(xml_text)
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