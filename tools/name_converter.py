import logging

from .base_tool import BaseTool
import re

logger = logging.getLogger(__name__)

class NameConverter(BaseTool):
    def __init__(self):
        super().__init__('命名格式转换器')

    def process(self, text: str) -> tuple:
        '''自动检测并转换命名格式'''
        is_snake = '_' in text and text.islower()
        is_camel = not is_snake and any(c.isupper() for c in text[1:])

        if is_snake:
            result = (self._to_camel(text), '下划线 → 驼峰')
            logger.info(f'转换下划线命名: "{text}" → "{result[0]}"')
            return result
        elif is_camel:
            result = (self._to_snake(text), '驼峰 → 下划线')
            logger.info(f'转换驼峰命名: "{text}" → "{result[0]}"')
            return result
        logger.debug('未检测到需要转换的命名格式: %s', text)
        return (text, '无需转换')

    def _to_camel(self, text: str) -> str:
        '''user_name → userName'''
        return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), text.lower())

    def _to_snake(self, text: str) -> str:
        '''userName → user_name'''
        text = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text).lower()

    def validate_input(self, text: str) -> bool:
        return bool(text.strip())

    def get_errors(self) -> list:
        return []

    def format_content(self):
        try:
            input_text = self.input_area.toPlainText()
            result, msg = self.process(input_text)
            self.output_area.setPlainText(result)
            logger.info(f'格式化成功: {msg}')
        except Exception as e:
            logger.error(f'格式化失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')