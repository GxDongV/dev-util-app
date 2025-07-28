# tools/xml_format.py
import xml.dom.minidom
from .base_tool import BaseTool

class XmlFormatTool(BaseTool):
    def __init__(self):
        super().__init__("XML 格式化")

    def format_content(self):
        try:
            dom = xml.dom.minidom.parseString(self.input_area.toPlainText())
            formatted = dom.toprettyxml(indent="  ")
            self.output_area.setText(formatted)
        except Exception as e:
            self.output_area.setText(f"XML 解析失败: {e}")