# tools/__init__.py

# 工具模块初始化文件
# 导入所有工具类，便于主程序统一加载

from .json_formatter import JsonFormatter
from .xml_formatter import XmlFormatter
from .base64_converter import Base64Converter
from .text_statistics import TextStatistics
from .name_converter import NameConverter
from .number_converter import NumberConverter

# 定义工具类列表，供主程序动态加载
TOOLS = [
    JsonFormatter,
    XmlFormatter,
    Base64Converter,
    TextStatistics,
    NameConverter,
    NumberConverter
]