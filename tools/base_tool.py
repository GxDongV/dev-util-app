# tools/base_tool.py
"""
基础工具类模块

定义所有工具的基类BaseTool，提供统一的接口和基础功能
所有具体工具类都应继承此类并实现抽象方法
"""
import logging
from abc import ABC, abstractmethod, ABCMeta
from PyQt5.QtWidgets import QWidget

# 配置日志记录
logger = logging.getLogger(__name__)


# 解决元类冲突：合并QWidget和ABCMeta的元类
class Meta(type(QWidget), ABCMeta):
    """
    元类用于解决多继承时的元类冲突问题
    合并QWidget的元类和ABCMeta抽象基类元类
    """
    pass


class BaseTool(QWidget, metaclass=Meta):
    """
    工具基类，所有功能工具的抽象父类

    提供统一的工具界面结构和基础功能，定义了工具类必须实现的抽象方法
    继承自QWidget以支持UI显示，使用自定义Meta元类解决元类冲突

    Attributes:
        name (str): 工具名称
        errors (list): 错误信息列表
    """
    def __init__(self, name: str):
        """
        初始化工具基类

        Args:
            name: 工具名称，用于标识和日志记录
        """
        super().__init__()
        self.name = name
        self.errors = []
        self.init_ui()

    def init_ui(self):
        """初始化工具UI界面

        子类可重写此方法来自定义界面布局
        默认实现为空
        """
        pass

    @abstractmethod
    def format_content(self):
        """格式化内容的抽象方法，子类必须实现

        通常用于将输入框内容进行处理并显示到输出框
        """
        pass

    # 基类异常处理框架
    def execute(self, text: str) -> tuple:
        """
        执行文本处理的包装方法，提供异常处理和日志记录

        Args:
            text: 输入文本

        Returns:
            tuple: 处理结果和状态消息，格式为(result, message)
                  成功时message为"成功"，失败时为错误信息
        """
        try:
            result = self.process(text)
            logger.info(f'{self.name} 执行成功 输入: {text} 输出: {result}')
            return result
        except Exception as e:
            logger.error(f'{self.name} 执行错误: {str(e)}', exc_info=True)
            return (f'处理出错: {str(e)}', '错误')

    def process(self, text: str):
        """处理文本的具体实现方法

        子类应重写此方法实现具体的文本处理逻辑

        Args:
            text: 输入文本

        Raises:
            NotImplementedError: 如果子类未实现此方法
        """
        raise NotImplementedError

    def get_errors(self) -> list:
        """获取错误信息列表

        Returns:
            list: 包含所有错误信息的列表
        """
        return self.errors
