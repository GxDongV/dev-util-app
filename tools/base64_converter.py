import base64
import hashlib
import hmac
import logging
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QMessageBox, \
    QLineEdit

from .base_tool import BaseTool
from .find_manager import FindManager
from .line_number_text_edit import LineNumberTextEdit
from .text_context_menu import TextContextMenu

logger = logging.getLogger(__name__)


class Base64Converter(BaseTool):
    def __init__(self):
        super().__init__('Base64加解码')
        self.find_manager = FindManager()

        # 创建输入输出框
        self.input_text = LineNumberTextEdit()
        self.input_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.input_text.customContextMenuRequested.connect(self.show_input_context_menu)

        self.output_area = LineNumberTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setContextMenuPolicy(Qt.CustomContextMenu)
        self.output_area.customContextMenuRequested.connect(self.show_output_context_menu)

        # 创建按钮
        self.encode_btn = QPushButton("转为base64")
        self.encode_btn.clicked.connect(self.encode)

        self.decode_btn = QPushButton("解码base64")
        self.decode_btn.clicked.connect(self.decode)

        # 添加MD5相关按钮
        self.md5_btn = QPushButton("计算MD5")
        self.md5_btn.clicked.connect(self.calculate_md5)

        self.md5_file_btn = QPushButton("文件MD5")
        self.md5_file_btn.clicked.connect(self.calculate_file_md5)

        # 添加SHA系列相关按钮
        self.sha256_btn = QPushButton("计算SHA-256")

        self.sha384_btn = QPushButton("计算SHA-384")

        self.sha512_btn = QPushButton("计算SHA-512")

        # 添加HMAC相关按钮
        self.hmacsha1_btn = QPushButton("计算HMAC-SHA1")

        self.hmacsha224_btn = QPushButton("计算HMAC-SHA224")

        # 添加图片相关按钮
        self.img_to_base64_btn = QPushButton("图片转Base64")
        self.img_to_base64_btn.clicked.connect(self.image_to_base64)

        self.base64_to_img_btn = QPushButton("Base64转图片")
        self.base64_to_img_btn.clicked.connect(self.base64_to_image)

        # HMAC密钥输入框
        self.hmac_key_input = QLineEdit()
        self.hmac_key_input.setPlaceholderText("输入HMAC密钥...")
        self.hmac_key_input.setEchoMode(QLineEdit.Password)

        # 连接SHA系列按钮信号
        self.sha256_btn.clicked.connect(lambda: self.calculate_sha("sha256"))
        self.sha384_btn.clicked.connect(lambda: self.calculate_sha("sha384"))
        self.sha512_btn.clicked.connect(lambda: self.calculate_sha("sha512"))

        # 连接HMAC系列按钮信号
        self.hmacsha1_btn.clicked.connect(lambda: self.calculate_hmac("sha1"))
        self.hmacsha224_btn.clicked.connect(lambda: self.calculate_hmac("sha224"))

        # 创建按钮网格布局，将相关功能按钮分组
        from PyQt5.QtWidgets import QGridLayout

        button_grid = QGridLayout()
        button_grid.setSpacing(10)

        # 第一列：Base64相关功能
        button_grid.addWidget(self.encode_btn, 0, 0)
        button_grid.addWidget(self.decode_btn, 1, 0)

        # 第二列：MD5相关功能
        button_grid.addWidget(self.md5_btn, 0, 1)
        button_grid.addWidget(self.md5_file_btn, 1, 1)

        # 第三列：SHA系列功能
        button_grid.addWidget(self.sha256_btn, 0, 2)
        button_grid.addWidget(self.sha384_btn, 1, 2)
        button_grid.addWidget(self.sha512_btn, 2, 2)

        # 第四列：HMAC系列功能
        button_grid.addWidget(self.hmacsha1_btn, 0, 3)
        button_grid.addWidget(self.hmacsha224_btn, 1, 3)
        button_grid.addWidget(self.hmac_key_input, 2, 3)

        # 第五列：图片相关功能
        button_grid.addWidget(self.img_to_base64_btn, 0, 4)
        button_grid.addWidget(self.base64_to_img_btn, 1, 4)

        # 添加伸展项使布局居中
        button_grid.setColumnStretch(5, 1)
        button_grid.setColumnMinimumWidth(0, 120)
        button_grid.setColumnMinimumWidth(1, 120)
        button_grid.setColumnMinimumWidth(2, 120)
        button_grid.setColumnMinimumWidth(3, 120)
        button_grid.setColumnMinimumWidth(4, 120)

        # 创建主布局并添加所有部件
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_grid)
        main_layout.addWidget(QLabel("输入内容:"))
        main_layout.addWidget(self.input_text)
        main_layout.addWidget(QLabel("处理结果:"))
        main_layout.addWidget(self.output_area)

        # 设置主布局
        self.setLayout(main_layout)

    def show_input_context_menu(self, position):
        """显示输入框的右键菜单"""
        TextContextMenu.show_context_menu(self.input_text, position, self.find_manager)

    def show_output_context_menu(self, position):
        """显示输出框的右键菜单"""
        TextContextMenu.show_context_menu(self.output_area, position, self.find_manager)

    def keyPressEvent(self, event):
        """处理键盘事件"""
        # 检查是否按下了Ctrl+F
        if event.matches(QKeySequence.Find):
            # 为主文本框显示查找对话框
            self.find_manager.show_find_dialog(self.input_text)
            return

        super().keyPressEvent(event)

    def encode(self):
        """将文本编码为Base64"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        try:
            # 转换为字节并编码
            encoded_bytes = base64.b64encode(input_text.encode('utf-8'))
            result = encoded_bytes.decode('utf-8')
            self.output_area.setPlainText(result)
            logger.info('Base64编码成功')
        except Exception as e:
            logger.error(f'Base64编码失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')

    def decode(self):
        """将Base64文本解码"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        try:
            # 解码Base64并转换为文本
            decoded_bytes = base64.b64decode(input_text.encode('utf-8'))
            result = decoded_bytes.decode('utf-8')
            self.output_area.setPlainText(result)
            logger.info('Base64解码成功')
        except Exception as e:
            logger.error(f'Base64解码失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')

    def format_content(self):
        """实现抽象方法，这里调用编码功能作为默认格式化操作"""
        self.encode()

    def calculate_md5(self):
        """计算输入文本的MD5值（同时显示16位和32位）"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        try:
            # 计算MD5
            md5_hash = hashlib.md5()
            md5_hash.update(input_text.encode('utf-8'))
            md5_32bit = md5_hash.hexdigest()  # 32位MD5
            md5_16bit = md5_32bit[8:24]  # 16位MD5（取中间16位）

            # 同时显示16位和32位MD5值
            result = f"16位: {md5_16bit}\n32位: {md5_32bit}"
            self.output_area.setPlainText(result)
            logger.info('MD5计算成功')
        except Exception as e:
            logger.error(f'MD5计算失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')

    def calculate_file_md5(self):
        """计算文件的MD5值（同时显示16位和32位）"""
        from PyQt5.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*);;")
        if not file_path:
            return

        try:
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as f:
                # 分块读取文件以处理大文件
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
            md5_32bit = md5_hash.hexdigest()  # 32位MD5
            md5_16bit = md5_32bit[8:24]  # 16位MD5（取中间16位）

            # 同时显示16位和32位MD5值
            result = f"16位: {md5_16bit}\n32位: {md5_32bit}"
            self.output_area.setPlainText(result)
            self.input_text.setPlainText(file_path)
            logger.info(f'文件MD5计算成功: {file_path}')
        except Exception as e:
            logger.error(f'文件MD5计算失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')

    def process(self, text: str):
        """实现BaseTool的抽象方法"""
        try:
            # 默认执行Base64编码
            encoded_bytes = base64.b64encode(text.encode('utf-8'))
            return encoded_bytes.decode('utf-8')
        except Exception as e:
            return f"处理出错: {str(e)}"

    def image_to_base64(self):
        """将图片转换为Base64编码"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif *.svg);;所有文件 (*)"
        )

        if not file_path:
            return

        try:
            # 读取图片文件并转换为Base64
            with open(file_path, "rb") as image_file:
                base64_data = base64.b64encode(image_file.read()).decode('utf-8')

            # 获取文件扩展名
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.png':
                mime_type = 'image/png'
            elif ext in ('.jpg', '.jpeg'):
                mime_type = 'image/jpeg'
            elif ext == '.bmp':
                mime_type = 'image/bmp'
            elif ext == '.gif':
                mime_type = 'image/gif'
            elif ext == '.svg':
                mime_type = 'image/svg+xml'
            else:
                mime_type = 'application/octet-stream'

            # 完整的Data URL格式
            data_url = f"data:{mime_type};base64,{base64_data}"

            self.output_area.setPlainText(data_url)
            self.input_text.setPlainText(file_path)
            logger.info(f'图片转换为Base64成功: {file_path}')
        except Exception as e:
            logger.error(f'图片转换为Base64失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')
            QMessageBox.critical(self, "错误", f"图片转换失败: {str(e)}")

    def base64_to_image(self):
        """将Base64编码转换为图片"""
        input_text = self.input_text.toPlainText().strip()
        if not input_text:
            QMessageBox.warning(self, "警告", "请输入Base64编码")
            return

        try:
            # 尝试提取Base64数据部分（如果是Data URL格式）
            if input_text.startswith('data:'):
                # 找到base64,的位置
                base64_start = input_text.find('base64,') + 7
                base64_data = input_text[base64_start:]
            else:
                base64_data = input_text

            # 解码Base64数据
            image_data = base64.b64decode(base64_data)

            # 保存为图片文件
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存图片", "", "PNG图片 (*.png);;JPEG图片 (*.jpg);;所有文件 (*)"
            )

            if not file_path:
                return

            # 确保文件有扩展名
            if not os.path.splitext(file_path)[1]:
                file_path += '.png'

            # 写入文件
            with open(file_path, 'wb') as f:
                f.write(image_data)

            self.output_area.setPlainText(f'图片已保存到: {file_path}')
            logger.info(f'Base64转换为图片成功，保存至: {file_path}')
            QMessageBox.information(self, "成功", f"图片已保存到: {file_path}")
        except Exception as e:
            logger.error(f'Base64转换为图片失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')
            QMessageBox.critical(self, "错误", f"Base64转换为图片失败: {str(e)}")

    def calculate_sha(self, algorithm):
        """计算输入文本的SHA哈希值"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        try:
            # 根据指定算法创建哈希对象
            if algorithm == "sha256":
                sha_hash = hashlib.sha256()
                algo_name = "SHA-256"
            elif algorithm == "sha384":
                sha_hash = hashlib.sha384()
                algo_name = "SHA-384"
            elif algorithm == "sha512":
                sha_hash = hashlib.sha512()
                algo_name = "SHA-512"
            else:
                raise ValueError(f"不支持的SHA算法: {algorithm}")

            # 更新哈希对象
            sha_hash.update(input_text.encode('utf-8'))
            result = sha_hash.hexdigest()

            self.output_area.setPlainText(f"{algo_name}: {result}")
            logger.info(f'{algo_name}计算成功')
        except Exception as e:
            logger.error(f'{algorithm}计算失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')

    def calculate_hmac(self, algorithm):
        """计算输入文本的HMAC哈希值"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            return

        # 获取HMAC密钥
        key = self.hmac_key_input.text()
        if not key:
            QMessageBox.warning(self, "警告", "请输入HMAC密钥")
            return

        try:
            # 根据指定算法创建HMAC对象
            if algorithm == "sha1":
                hmac_hash = hmac.new(key.encode('utf-8'), input_text.encode('utf-8'), hashlib.sha1)
                algo_name = "HMAC-SHA1"
            elif algorithm == "sha224":
                hmac_hash = hmac.new(key.encode('utf-8'), input_text.encode('utf-8'), hashlib.sha224)
                algo_name = "HMAC-SHA224"
            else:
                raise ValueError(f"不支持的HMAC算法: {algorithm}")

            # 获取HMAC结果
            result = hmac_hash.hexdigest()

            self.output_area.setPlainText(f"{algo_name}: {result}")
            logger.info(f'{algo_name}计算成功')
        except Exception as e:
            logger.error(f'{algorithm}计算失败: {str(e)}')
            self.output_area.setPlainText(f'错误: {str(e)}')