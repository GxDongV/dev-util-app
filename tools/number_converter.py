# tools/number_converter.py

import logging
import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QGridLayout, QFrame, QLineEdit

from .base_tool import BaseTool
from .find_manager import FindManager
from .line_number_text_edit import LineNumberTextEdit
from .text_context_menu import TextContextMenu

logger = logging.getLogger(__name__)

# 北约字母表映射
NATO_ALPHABET = {
    '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four',
    '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'
}

# 宽体字映射
WIDE_CHARACTERS = {
    '0': '０', '1': '１', '2': '２', '3': '３', '4': '４',
    '5': '５', '6': '６', '7': '７', '8': '８', '9': '９'
}

# 罗马数字映射
ROMAN_NUMERALS = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
]

# 英文数字映射
ONES = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
        'seventeen', 'eighteen', 'nineteen']
TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

# ASCII控制字符名称映射（包含中英文说明）
ASCII_CONTROL_CHARS = {
    0: ('NUL', '空字符'),
    1: ('SOH', '标题开始'),
    2: ('STX', '正文开始'),
    3: ('ETX', '正文结束'),
    4: ('EOT', '传输结束'),
    5: ('ENQ', '询问字符'),
    6: ('ACK', '确认字符'),
    7: ('BEL', '响铃字符'),
    8: ('BS', '退格字符'),
    9: ('HT', '水平制表符'),
    10: ('LF', '换行符'),
    11: ('VT', '垂直制表符'),
    12: ('FF', '换页符'),
    13: ('CR', '回车符'),
    14: ('SO', '移出'),
    15: ('SI', '移入'),
    16: ('DLE', '数据链路转义'),
    17: ('DC1', '设备控制1'),
    18: ('DC2', '设备控制2'),
    19: ('DC3', '设备控制3'),
    20: ('DC4', '设备控制4'),
    21: ('NAK', '否定确认'),
    22: ('SYN', '同步空闲'),
    23: ('ETB', '传输块结束'),
    24: ('CAN', '取消字符'),
    25: ('EM', '介质终止'),
    26: ('SUB', '替换字符'),
    27: ('ESC', '转义字符'),
    28: ('FS', '文件分隔符'),
    29: ('GS', '组分隔符'),
    30: ('RS', '记录分隔符'),
    31: ('US', '单元分隔符'),
    32: ('SP', '空格'),
    127: ('DEL', '删除字符')
}

# 存储单位映射
STORAGE_UNITS = [
    ('bit', '比特'),
    ('B', '字节'),
    ('KB', '千字节'),
    ('MB', '兆字节'),
    ('GB', '千兆字节'),
    ('TB', '太字节'),
    ('PB', '拍字节'),
    ('EB', '艾字节')
]


class NumberConverter(BaseTool):
    def __init__(self):
        super().__init__('数字转换工具')
        self.find_manager = FindManager()
        
        # 创建输入文本框
        self.input_text = LineNumberTextEdit()
        self.input_text.textChanged.connect(self.update_conversions)
        self.input_text.setPlaceholderText("请输入数字...")
        self.input_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.input_text.customContextMenuRequested.connect(self.show_input_context_menu)
        
        # 创建转换结果显示区域
        self.results_frame = QFrame()
        self.results_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        results_layout = QGridLayout(self.results_frame)
        
        # 设置列伸缩属性
        results_layout.setColumnStretch(0, 1)  # 标签列
        results_layout.setColumnStretch(1, 2)  # 数值列
        results_layout.setColumnStretch(2, 1)  # 第二标签列
        results_layout.setColumnStretch(3, 2)  # 第二数值列
        
        # 初始化结果显示框
        # 使用QLineEdit并设置为只读，这样用户可以选中和复制内容
        self.digit_count_label = QLineEdit()
        self.digit_count_label.setReadOnly(True)
        self.line_count_label = QLineEdit()
        self.line_count_label.setReadOnly(True)
        self.byte_size_label = QLineEdit()
        self.byte_size_label.setReadOnly(True)
        self.min_digit_label = QLineEdit()
        self.min_digit_label.setReadOnly(True)
        self.max_digit_label = QLineEdit()
        self.max_digit_label.setReadOnly(True)
        self.avg_digit_label = QLineEdit()
        self.avg_digit_label.setReadOnly(True)
        self.nato_label = QLineEdit()
        self.nato_label.setReadOnly(True)
        self.wide_label = QLineEdit()
        self.wide_label.setReadOnly(True)
        self.ascii_label = QLineEdit()
        self.ascii_label.setReadOnly(True)
        self.grouped_label = QLineEdit()
        self.grouped_label.setReadOnly(True)
        self.reversed_label = QLineEdit()
        self.reversed_label.setReadOnly(True)
        self.english_label = QLineEdit()
        self.english_label.setReadOnly(True)
        self.scientific_label = QLineEdit()
        self.scientific_label.setReadOnly(True)
        self.binary_label = QLineEdit()
        self.binary_label.setReadOnly(True)
        self.octal_label = QLineEdit()
        self.octal_label.setReadOnly(True)
        self.decimal_label = QLineEdit()
        self.decimal_label.setReadOnly(True)
        self.hexadecimal_label = QLineEdit()
        self.hexadecimal_label.setReadOnly(True)
        self.roman_label = QLineEdit()
        self.roman_label.setReadOnly(True)
        
        # 存储单位换算结果显示框（可输入）
        self.bit_input = QLineEdit()
        self.bit_input.textChanged.connect(lambda text: self.on_storage_unit_changed(text, 'bit'))
        self.byte_input = QLineEdit()
        self.byte_input.textChanged.connect(lambda text: self.on_storage_unit_changed(text, 'B'))
        self.kb_input = QLineEdit()
        self.kb_input.textChanged.connect(lambda text: self.on_storage_unit_changed(text, 'KB'))
        self.mb_input = QLineEdit()
        self.mb_input.textChanged.connect(lambda text: self.on_storage_unit_changed(text, 'MB'))
        self.gb_input = QLineEdit()
        self.gb_input.textChanged.connect(lambda text: self.on_storage_unit_changed(text, 'GB'))
        self.tb_input = QLineEdit()
        self.tb_input.textChanged.connect(lambda text: self.on_storage_unit_changed(text, 'TB'))
        self.pb_input = QLineEdit()
        self.pb_input.textChanged.connect(lambda text: self.on_storage_unit_changed(text, 'PB'))
        self.eb_input = QLineEdit()
        self.eb_input.textChanged.connect(lambda text: self.on_storage_unit_changed(text, 'EB'))
        
        # 添加标签到布局（两列显示）
        # 第一行：数字个数和行数
        results_layout.addWidget(QLabel("数字个数:"), 0, 0)
        results_layout.addWidget(self.digit_count_label, 0, 1)
        results_layout.addWidget(QLabel("行数:"), 0, 2)
        results_layout.addWidget(self.line_count_label, 0, 3)
        
        # 第二行：字节大小和最小数字
        results_layout.addWidget(QLabel("字节大小:"), 1, 0)
        results_layout.addWidget(self.byte_size_label, 1, 1)
        results_layout.addWidget(QLabel("最小数字:"), 1, 2)
        results_layout.addWidget(self.min_digit_label, 1, 3)
        
        # 第三行：最大数字和平均值
        results_layout.addWidget(QLabel("最大数字:"), 2, 0)
        results_layout.addWidget(self.max_digit_label, 2, 1)
        results_layout.addWidget(QLabel("平均值:"), 2, 2)
        results_layout.addWidget(self.avg_digit_label, 2, 3)
        
        # 第四行：北约字母表和宽体字
        results_layout.addWidget(QLabel("北约字母表:"), 3, 0)
        results_layout.addWidget(self.nato_label, 3, 1)
        results_layout.addWidget(QLabel("宽体字:"), 3, 2)
        results_layout.addWidget(self.wide_label, 3, 3)
        
        # 第五行：ASCII码和千位分组
        results_layout.addWidget(QLabel("ASCII码:"), 4, 0)
        results_layout.addWidget(self.ascii_label, 4, 1)
        results_layout.addWidget(QLabel("千位分组:"), 4, 2)
        results_layout.addWidget(self.grouped_label, 4, 3)
        
        # 第六行：数字反转和英文表示
        results_layout.addWidget(QLabel("数字反转:"), 5, 0)
        results_layout.addWidget(self.reversed_label, 5, 1)
        results_layout.addWidget(QLabel("英文表示:"), 5, 2)
        results_layout.addWidget(self.english_label, 5, 3)
        
        # 第七行：科学计数法和二进制
        results_layout.addWidget(QLabel("科学计数法:"), 6, 0)
        results_layout.addWidget(self.scientific_label, 6, 1)
        results_layout.addWidget(QLabel("二进制:"), 6, 2)
        results_layout.addWidget(self.binary_label, 6, 3)
        
        # 第八行：八进制和十进制
        results_layout.addWidget(QLabel("八进制:"), 7, 0)
        results_layout.addWidget(self.octal_label, 7, 1)
        results_layout.addWidget(QLabel("十进制:"), 7, 2)
        results_layout.addWidget(self.decimal_label, 7, 3)
        
        # 第九行：十六进制和罗马数字
        results_layout.addWidget(QLabel("十六进制:"), 8, 0)
        results_layout.addWidget(self.hexadecimal_label, 8, 1)
        results_layout.addWidget(QLabel("罗马数字:"), 8, 2)
        results_layout.addWidget(self.roman_label, 8, 3)
        
        # 存储单位换算标签（两列显示）
        results_layout.addWidget(QLabel("存储单位换算:"), 9, 0, 1, 4)  # 跨4列
        results_layout.addWidget(QLabel("比特(bit):"), 10, 0)
        results_layout.addWidget(self.bit_input, 10, 1)
        results_layout.addWidget(QLabel("字节(B):"), 10, 2)
        results_layout.addWidget(self.byte_input, 10, 3)
        
        results_layout.addWidget(QLabel("千字节(KB):"), 11, 0)
        results_layout.addWidget(self.kb_input, 11, 1)
        results_layout.addWidget(QLabel("兆字节(MB):"), 11, 2)
        results_layout.addWidget(self.mb_input, 11, 3)
        
        results_layout.addWidget(QLabel("千兆字节(GB):"), 12, 0)
        results_layout.addWidget(self.gb_input, 12, 1)
        results_layout.addWidget(QLabel("太字节(TB):"), 12, 2)
        results_layout.addWidget(self.tb_input, 12, 3)
        
        results_layout.addWidget(QLabel("拍字节(PB):"), 13, 0)
        results_layout.addWidget(self.pb_input, 13, 1)
        results_layout.addWidget(QLabel("艾字节(EB):"), 13, 2)
        results_layout.addWidget(self.eb_input, 13, 3)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("输入数字:"))
        main_layout.addWidget(self.input_text)
        main_layout.addWidget(QLabel("转换结果:"))
        main_layout.addWidget(self.results_frame)
        
        # 设置主布局
        self.setLayout(main_layout)
        
        # 初始化转换结果
        self.update_conversions()

    def show_input_context_menu(self, position):
        """显示输入框的右键菜单"""
        TextContextMenu.show_context_menu(self.input_text, position, self.find_manager)
        
    def keyPressEvent(self, event):
        """处理键盘事件"""
        # 检查是否按下了Ctrl+F
        if event.matches(QKeySequence.Find):
            # 为主文本框显示查找对话框
            self.find_manager.show_find_dialog(self.input_text)
            return
            
        super().keyPressEvent(event)

    def extract_digits(self, text):
        """提取文本中的所有数字"""
        return re.findall(r'\d', text)

    def count_lines(self, text):
        """统计行数"""
        if not text:
            return 0
        return text.count('\n') + 1

    def get_min_digit(self, digits):
        """获取最小数字"""
        if not digits:
            return ""
        return min(digits)

    def get_max_digit(self, digits):
        """获取最大数字"""
        if not digits:
            return ""
        return max(digits)

    def get_avg_digit(self, digits):
        """计算数字平均值"""
        if not digits:
            return ""
        try:
            digit_values = [int(d) for d in digits]
            return str(round(sum(digit_values) / len(digit_values), 2))
        except:
            return "计算错误"

    def to_nato_alphabet(self, digits):
        """转换为北约字母表"""
        return ' '.join([NATO_ALPHABET[digit] for digit in digits])

    def to_wide_characters(self, digits):
        """转换为宽体字"""
        return ''.join([WIDE_CHARACTERS[digit] for digit in digits])

    def to_ascii(self, digits):
        """转换为ASCII码表示"""
        if not digits:
            return ""
        
        try:
            # 将所有数字连接成一个数字字符串
            number_str = ''.join(digits)
            if not number_str:
                return ""
            
            # 转换为整数
            number = int(number_str)
            
            # 检查ASCII范围 (0-127)
            if 0 <= number <= 127:
                # 对于控制字符，使用标准名称和中文说明
                if number in ASCII_CONTROL_CHARS:
                    char_code, description = ASCII_CONTROL_CHARS[number]
                    return f"{number}({char_code}-{description})"
                else:
                    # 对于可打印字符，直接显示字符
                    ascii_char = chr(number)
                    return f"{number}({ascii_char})"
            else:
                return f"{number}(超出ASCII范围0-127)"
        except ValueError:
            return "无效输入"
        except Exception as e:
            return f"转换错误: {str(e)}"

    def convert_storage_units(self, bits):
        """存储单位换算"""
        try:
            # 各种单位换算 (1字节=8比特, 1KB=1024字节, 以此类推)
            bytes_val = bits / 8
            kb_val = bytes_val / 1024
            mb_val = kb_val / 1024
            gb_val = mb_val / 1024
            tb_val = gb_val / 1024
            pb_val = tb_val / 1024
            eb_val = pb_val / 1024
            
            # 格式化显示结果，根据数值大小选择合适的格式
            def format_value(value):
                if value == 0:
                    return "0"
                elif value < 0.001:
                    return f"{value:.2e}"
                elif value < 1:
                    return f"{value:.3f}"
                elif value == int(value):  # 整数不显示小数点
                    return str(int(value))
                elif value < 1000:
                    return f"{value:.2f}"
                else:
                    # 对于大数值，使用千位分组但保持小数
                    return f"{value:,.2f}"
            
            return [
                format_value(bits),
                format_value(bytes_val),
                format_value(kb_val),
                format_value(mb_val),
                format_value(gb_val),
                format_value(tb_val),
                format_value(pb_val),
                format_value(eb_val)
            ]
        except Exception as e:
            return [f"转换错误: {str(e)}"] * 8

    def on_storage_unit_changed(self, text, unit):
        """当存储单位输入框内容改变时触发"""
        if not text:
            return
            
        try:
            # 解析输入的数值
            value = float(text)
            
            # 根据不同的单位计算出比特数
            bits = 0
            if unit == 'bit':
                bits = value
            elif unit == 'B':
                bits = value * 8
            elif unit == 'KB':
                bits = value * 1024 * 8
            elif unit == 'MB':
                bits = value * 1024 * 1024 * 8
            elif unit == 'GB':
                bits = value * 1024 * 1024 * 1024 * 8
            elif unit == 'TB':
                bits = value * 1024 * 1024 * 1024 * 1024 * 8
            elif unit == 'PB':
                bits = value * 1024 * 1024 * 1024 * 1024 * 1024 * 8
            elif unit == 'EB':
                bits = value * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 8
            
            # 计算所有单位的值
            results = self.convert_storage_units(bits)
            bit_result, byte_result, kb_result, mb_result, gb_result, tb_result, pb_result, eb_result = results
            
            # 更新所有输入框，避免触发递归更新
            self.bit_input.blockSignals(True)
            self.byte_input.blockSignals(True)
            self.kb_input.blockSignals(True)
            self.mb_input.blockSignals(True)
            self.gb_input.blockSignals(True)
            self.tb_input.blockSignals(True)
            self.pb_input.blockSignals(True)
            self.eb_input.blockSignals(True)
            
            self.bit_input.setText(bit_result)
            self.byte_input.setText(byte_result)
            self.kb_input.setText(kb_result)
            self.mb_input.setText(mb_result)
            self.gb_input.setText(gb_result)
            self.tb_input.setText(tb_result)
            self.pb_input.setText(pb_result)
            self.eb_input.setText(eb_result)
            
            # 恢复信号
            self.bit_input.blockSignals(False)
            self.byte_input.blockSignals(False)
            self.kb_input.blockSignals(False)
            self.mb_input.blockSignals(False)
            self.gb_input.blockSignals(False)
            self.tb_input.blockSignals(False)
            self.pb_input.blockSignals(False)
            self.eb_input.blockSignals(False)
            
        except ValueError:
            # 输入不是有效数字，不做处理
            pass
        except Exception as e:
            # 其他异常，不做处理
            pass

    def to_grouped(self, digits):
        """千位分组显示"""
        if not digits:
            return ""
        try:
            number = int(''.join(digits))
            return f"{number:,}"
        except ValueError:
            return "无效输入"

    def to_reversed(self, digits):
        """数字顺序反转"""
        if not digits:
            return ""
        return ''.join(reversed(digits))

    def to_english(self, digits):
        """将数字转换为英文单词"""
        if not digits:
            return ""
        try:
            number = int(''.join(digits))
            # 限制处理范围，避免复杂计算
            if number > 999999:
                return "超出处理范围(最大999999)"
            if number == 0:
                return "zero"
            if number < 0:
                return "negative " + self._convert_hundreds(-number)
            return self._convert_large_number(number)
        except ValueError:
            return "无效输入"

    def _convert_large_number(self, num):
        """转换大数字为英文"""
        if num == 0:
            return "zero"
        
        if num < 1000:
            return self._convert_hundreds(num)
        
        result = ""
        if num >= 1000:
            thousands = num // 1000
            remainder = num % 1000
            result += self._convert_hundreds(thousands) + " thousand"
            if remainder > 0:
                result += " " + self._convert_hundreds(remainder)
        
        return result

    def _convert_hundreds(self, num):
        """转换小于1000的数字为英文"""
        if num == 0:
            return ""
        
        result = ""
        
        # 处理百位
        if num >= 100:
            result += ONES[num // 100] + " hundred"
            num %= 100
            if num > 0:
                result += " "
        
        # 处理十位和个位
        if num >= 20:
            tens_digit = num // 10
            ones_digit = num % 10
            result += TENS[tens_digit]
            if ones_digit > 0:
                result += "-" + ONES[ones_digit]
        elif num > 0:
            result += ONES[num]
        
        return result

    def to_scientific(self, digits):
        """转换为科学计数法"""
        if not digits:
            return ""
        try:
            number = int(''.join(digits))
            return f"{number:.2e}"
        except ValueError:
            return "无效输入"

    def to_binary(self, digits):
        """转换为二进制表示"""
        if not digits:
            return ""
        # 将所有数字连接成一个数字字符串，然后转换为整数再转二进制
        try:
            number = int(''.join(digits))
            return bin(number)[2:]  # 去掉'0b'前缀
        except ValueError:
            return "无效输入"

    def to_octal(self, digits):
        """转换为八进制表示"""
        if not digits:
            return ""
        try:
            number = int(''.join(digits))
            return oct(number)[2:]  # 去掉'0o'前缀
        except ValueError:
            return "无效输入"

    def to_decimal(self, digits):
        """转换为十进制表示"""
        if not digits:
            return ""
        try:
            number = int(''.join(digits))
            return str(number)
        except ValueError:
            return "无效输入"

    def to_hexadecimal(self, digits):
        """转换为十六进制表示"""
        if not digits:
            return ""
        try:
            number = int(''.join(digits))
            return hex(number)[2:].upper()  # 去掉'0x'前缀并转为大写
        except ValueError:
            return "无效输入"

    def to_roman(self, digits):
        """转换为罗马数字"""
        if not digits:
            return ""
        try:
            number = int(''.join(digits))
            if number <= 0 or number > 3999:
                return "超出范围(1-3999)"
            
            result = ""
            for value, numeral in ROMAN_NUMERALS:
                count = number // value
                result += numeral * count
                number -= value * count
            return result
        except ValueError:
            return "无效输入"

    def update_conversions(self):
        """更新转换结果"""
        text = self.input_text.toPlainText()
        
        # 提取数字
        digits = self.extract_digits(text)
        
        # 计算各种转换结果
        digit_count = len(digits)
        line_count = self.count_lines(text)
        byte_size = len(text.encode('utf-8'))
        min_digit = self.get_min_digit(digits)
        max_digit = self.get_max_digit(digits)
        avg_digit = self.get_avg_digit(digits)
        nato_result = self.to_nato_alphabet(digits) if digits else ""
        wide_result = self.to_wide_characters(digits) if digits else ""
        ascii_result = self.to_ascii(digits) if digits else ""
        grouped_result = self.to_grouped(digits) if digits else ""
        reversed_result = self.to_reversed(digits) if digits else ""
        english_result = self.to_english(digits) if digits else ""
        scientific_result = self.to_scientific(digits) if digits else ""
        binary_result = self.to_binary(digits)
        octal_result = self.to_octal(digits)
        decimal_result = self.to_decimal(digits)
        hexadecimal_result = self.to_hexadecimal(digits)
        roman_result = self.to_roman(digits)
        
        # 存储单位换算（基于输入的数字）
        if digits:
            try:
                number_str = ''.join(digits)
                if number_str:
                    bits = float(number_str)
                    storage_results = self.convert_storage_units(bits)
                    bit_result, byte_result, kb_result, mb_result, gb_result, tb_result, pb_result, eb_result = storage_results
                    
                    # 更新存储单位输入框
                    self.bit_input.setText(bit_result)
                    self.byte_input.setText(byte_result)
                    self.kb_input.setText(kb_result)
                    self.mb_input.setText(mb_result)
                    self.gb_input.setText(gb_result)
                    self.tb_input.setText(tb_result)
                    self.pb_input.setText(pb_result)
                    self.eb_input.setText(eb_result)
            except:
                # 如果转换失败，清空存储单位输入框
                self.bit_input.setText("")
                self.byte_input.setText("")
                self.kb_input.setText("")
                self.mb_input.setText("")
                self.gb_input.setText("")
                self.tb_input.setText("")
                self.pb_input.setText("")
                self.eb_input.setText("")
        else:
            # 如果没有数字，清空存储单位输入框
            self.bit_input.setText("")
            self.byte_input.setText("")
            self.kb_input.setText("")
            self.mb_input.setText("")
            self.gb_input.setText("")
            self.tb_input.setText("")
            self.pb_input.setText("")
            self.eb_input.setText("")
        
        # 更新标签显示
        self.digit_count_label.setText(str(digit_count))
        self.line_count_label.setText(str(line_count))
        self.byte_size_label.setText(str(byte_size) + " bytes")
        self.min_digit_label.setText(min_digit)
        self.max_digit_label.setText(max_digit)
        self.avg_digit_label.setText(avg_digit)
        self.nato_label.setText(nato_result)
        self.wide_label.setText(wide_result)
        self.ascii_label.setText(ascii_result)
        self.grouped_label.setText(grouped_result)
        self.reversed_label.setText(reversed_result)
        self.english_label.setText(english_result)
        self.scientific_label.setText(scientific_result)
        self.binary_label.setText(binary_result)
        self.octal_label.setText(octal_result)
        self.decimal_label.setText(decimal_result)
        self.hexadecimal_label.setText(hexadecimal_result)
        self.roman_label.setText(roman_result)

    def format_content(self):
        """实现抽象方法"""
        self.update_conversions()
    
    def process(self, text: str):
        """实现BaseTool的抽象方法"""
        try:
            # 提取数字
            digits = self.extract_digits(text)
            
            # 计算各种转换结果
            digit_count = len(digits)
            line_count = self.count_lines(text)
            byte_size = len(text.encode('utf-8'))
            min_digit = self.get_min_digit(digits)
            max_digit = self.get_max_digit(digits)
            avg_digit = self.get_avg_digit(digits)
            nato_result = self.to_nato_alphabet(digits) if digits else ""
            wide_result = self.to_wide_characters(digits) if digits else ""
            ascii_result = self.to_ascii(digits) if digits else ""
            grouped_result = self.to_grouped(digits) if digits else ""
            reversed_result = self.to_reversed(digits) if digits else ""
            english_result = self.to_english(digits) if digits else ""
            scientific_result = self.to_scientific(digits) if digits else ""
            binary_result = self.to_binary(digits)
            octal_result = self.to_octal(digits)
            decimal_result = self.to_decimal(digits)
            hexadecimal_result = self.to_hexadecimal(digits)
            roman_result = self.to_roman(digits)
            
            # 存储单位换算
            storage_results = [""] * 8
            if digits:
                try:
                    number_str = ''.join(digits)
                    if number_str:
                        bits = float(number_str)
                        storage_results = self.convert_storage_units(bits)
                except:
                    pass
            
            bit_result, byte_result, kb_result, mb_result, gb_result, tb_result, pb_result, eb_result = storage_results
            
            result = f"""数字个数: {digit_count}
行数: {line_count}
字节大小: {byte_size} bytes
最小数字: {min_digit}
最大数字: {max_digit}
平均值: {avg_digit}
北约字母表: {nato_result}
宽体字: {wide_result}
ASCII码: {ascii_result}
千位分组: {grouped_result}
数字反转: {reversed_result}
英文表示: {english_result}
科学计数法: {scientific_result}
二进制: {binary_result}
八进制: {octal_result}
十进制: {decimal_result}
十六进制: {hexadecimal_result}
罗马数字: {roman_result}
存储单位换算:
比特(bit): {bit_result}
字节(B): {byte_result}
千字节(KB): {kb_result}
兆字节(MB): {mb_result}
千兆字节(GB): {gb_result}
太字节(TB): {tb_result}
拍字节(PB): {pb_result}
艾字节(EB): {eb_result}"""
            return result
        except Exception as e:
            return f"处理出错: {str(e)}"