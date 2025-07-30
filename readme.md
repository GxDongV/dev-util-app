# 开发工具集 (devUtilsApp)

一个面向开发者的实用工具集合，旨在提供常见的数据格式化与验证功能，如JSON和XML，简化开发过程中的调试和处理操作。

## 功能特性

- JSON格式化与验证
- XML格式化与验证
- Base64编码/解码
- 命名格式转换（驼峰、下划线、帕斯卡命名等）
- 支持深色/浅色主题切换

## 技术栈

- Python 3.8+
- PyQt5 v5.15.7
- qdarkstyle

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python main.py
```

## 打包为exe可执行文件

### 方法一：使用PyInstaller命令（推荐）

```bash
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --hidden-import=qdarkstyle --hidden-import=qdarkstyle.dark.palette --hidden-import=qdarkstyle.light.palette --add-data "ui;ui" --add-data "tools;tools" main.py
```

打包完成后，可执行文件位于 `dist/main/main.exe`

### 方法二：使用打包脚本

```bash
python build_exe.py
```

## 目录结构

```
devUtilsApp/
├── main.py              # 程序入口
├── requirements.txt     # 依赖文件
├── readme.md            # 说明文档
├── build_exe.py         # 打包脚本
├── ui/                  # 界面模块
│   └── main_window.py   # 主窗口
├── tools/               # 工具模块
│   ├── base_tool.py     # 工具基类
│   ├── json_formatter.py# JSON格式化工具
│   ├── xml_formatter.py # XML格式化工具
│   ├── base64_converter.py # Base64转换工具
│   └── name_converter.py# 命名转换工具
└── dist/                # 打包输出目录
    └── main/            # 打包结果
        ├── main.exe     # 可执行文件
        └── _internal/   # 依赖文件
```

## 使用说明

1. 运行程序后，通过左侧导航栏选择需要的工具
2. 在工具界面中输入相应内容
3. 点击工具按钮执行操作
4. 可通过右下角按钮切换深色/浅色主题

## 注意事项

- 打包后的程序会生成一个文件夹，包含exe文件和依赖文件
- 如需单独的exe文件（无文件夹），可使用 `--onefile` 参数替换 `--onedir`
- 打包为单个exe文件启动较慢，但分发更简单
