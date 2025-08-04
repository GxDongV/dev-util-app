# 开发工具集 (devUtilsApp)

一个面向开发者的实用工具集合，旨在提供常见的数据格式化与验证功能，如JSON和XML，简化开发过程中的调试和处理操作。

## 功能特性

- JSON格式化与验证
- XML格式化与验证
- Base64编码/解码
- 命名格式转换（驼峰、下划线、帕斯卡命名等）
- 文本统计（字数、字符数、汉字数等统计）
- 支持深色/浅色主题切换

## 技术栈

- Python 3.8+
- PyQt5 v5.15.7
- qdarkstyle v3.2.3
- Pillow v10.0.0+

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python main.py
```

## 设置应用程序图标

图标文件已包含在项目中：
- `resources/app_icon.ico`：应用程序图标文件
- `resources/app_icon.png`：应用程序图标(PNG格式)

## 打包为exe可执行文件与安装包

### 方法一：使用打包脚本构建单文件安装包

```bash
python build_installer.py
```

此脚本将：
1. 使用PyInstaller将项目打包为单文件exe
2. 创建NSIS和Inno Setup安装包
3. 安装包输出到 `installer/DevUtilsApp_Setup.exe`

### 方法二：使用打包脚本构建多文件安装包

```bash
python build_multi_file_installer.py
```

此脚本将：
1. 使用PyInstaller将项目打包为多文件形式
2. 创建Inno Setup安装包
3. 安装包输出到 `installer/DevUtilsApp_Setup.exe`

### 方法三：手动使用PyInstaller命令

单文件模式：
```bash
pyinstaller --noconfirm --onefile --windowed --hidden-import=qdarkstyle --hidden-import=qdarkstyle.dark.palette --hidden-import=qdarkstyle.light.palette --hidden-import=qdarkstyle.dark.stylesheet --hidden-import=qdarkstyle.light.stylesheet --hidden-import=qdarkstyle.utils --add-data "ui;ui" --add-data "tools;tools" --add-data "resources;resources" --icon "resources/app_icon.ico" main.py
```

多文件模式：
```bash
pyinstaller --noconfirm --windowed --hidden-import=qdarkstyle --hidden-import=qdarkstyle.dark.palette --hidden-import=qdarkstyle.light.palette --hidden-import=qdarkstyle.dark.stylesheet --hidden-import=qdarkstyle.light.stylesheet --hidden-import=qdarkstyle.utils --add-data "ui;ui" --add-data "tools;tools" --add-data "resources;resources" --icon "resources/app_icon.ico" --name main main.py
```

## 目录结构

```
devUtilsApp/
├── main.py                      # 程序入口
├── build_installer.py           # 安装包构建脚本（支持单文件和多文件打包）
├── build_multi_file_installer.py # 多文件模式安装包构建脚本
├── requirements.txt             # 依赖文件
├── readme.md                    # 说明文档
├── developDocument.md           # 开发文档
├── installer/                   # 安装包输出目录
│   └── DevUtilsApp_Setup.exe    # 生成的安装包
├── resources/                   # 资源文件目录
│   ├── app_icon.ico             # 应用程序图标文件
│   └── app_icon.png             # 应用程序图标(PNG格式)
├── setup.iss                    # Inno Setup安装脚本
├── setup.nsi                    # NSIS安装脚本
├── tools/                       # 工具模块
│   ├── __init__.py              # Python包初始化文件
│   ├── base_tool.py             # 工具基类
│   ├── json_formatter.py        # JSON格式化工具
│   ├── xml_formatter.py         # XML格式化工具
│   ├── base64_converter.py      # Base64转换工具
│   ├── name_converter.py        # 命名转换工具
│   ├── number_converter.py      # 数字转换工具
│   ├── text_context_menu.py     # 文本上下文菜单
│   ├── text_statistics.py       # 文本统计工具
│   ├── line_number_text_edit.py # 带行号的文本编辑器
│   ├── find_dialog.py           # 查找对话框
│   └── find_manager.py          # 查找管理器
├── ui/                          # 界面模块
│   └── main_window.py           # 主窗口
└── dist/                        # 打包输出目录
    └── main/                    # 多文件打包结果
        ├── main.exe             # 可执行文件
        └── _internal/           # 依赖文件
```

## 使用说明

1. 运行程序后，通过左侧导航栏选择需要的工具
2. 在工具界面中输入相应内容
3. 点击工具按钮执行操作
4. 可通过右下角按钮切换深色/浅色主题

## 工具详细说明

### 文本统计工具
文本统计工具可以对输入的文本进行详细统计，包括：
- 总字数：文本中字符的总数
- 总字符数：文本中单词的总数
- 总汉字数：文本中汉字的数量
- 汉字符号：文本中中文标点符号的数量

## 注意事项
- 多文件模式打包的程序启动速度更快，但分发相对复杂
- 单文件模式打包的程序分发更简单，但启动速度较慢
- 安装包会将程序安装到系统中，并创建桌面快捷方式
- 日志文件会保存在用户的文档目录下的DevUtilsApp文件夹中，避免权限问题