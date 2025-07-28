# tools/json_format.py
import json
from .base_tool import BaseTool

class JsonFormatTool(BaseTool):
    def __init__(self):
        super().__init__("JSON 格式化")

    def format_content(self):
        try:
            data = json.loads(self.input_area.toPlainText())
            formatted = json.dumps(data, indent=2, ensure_ascii=False)
            self.output_area.setText(formatted)
        except json.JSONDecodeError as e:
            self.output_area.setText(f"JSON 解析失败: {e}")