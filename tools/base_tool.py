# tools/base_tool.py
"""
基础工具类模块

定义所有工具的基类BaseTool，提供统一的接口和基础功能
所有具体工具类都应继承此类并实现抽象方法
"""
import logging
from abc import abstractmethod

from PyQt5.QtWidgets import QWidget

# 配置日志记录
logger = logging.getLogger(__name__)

from abc import ABCMeta

# 解决元类冲突：合并QWidget和ABCMeta的元类
class Meta(type(QWidget), ABCMeta):
    pass

class BaseTool(QWidget, metaclass=Meta):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.errors = []
        self.init_ui()

    def init_ui(self):
        pass

    @abstractmethod
    def format_content(self):
        """子类需实现具体的格式化逻辑"""
        pass

    # 基类异常处理框架
    def execute(self, text: str):
        try:
            result = self.process(text)
            logger.info(f'{self.name} 执行成功 输入: {text} 输出: {result}')
            return result
        except Exception as e:
            logger.error(f'{self.name} 执行错误: {str(e)}', exc_info=True)
            return (f'处理出错: {str(e)}', '错误')

    def process(self, text: str):
        raise NotImplementedError

    def get_errors(self):
        return self.errors
