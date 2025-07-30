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
- qdarkstyle

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python main.py
```

## 设置应用程序图标

1. 创建应用程序图标文件：
   - 准备一个ICO格式的图标文件，命名为 `app_icon.ico`
   - 推荐尺寸包括：16x16, 32x32, 48x48, 64x64, 128x128, 256x256
   - 将图标文件放置在 `resources` 目录中

2. （可选）准备一个PNG格式的图标文件用于界面显示：
   - 命名为 `app_icon.png`
   - 推荐尺寸：64x64 或 128x128
   - 将图标文件放置在 `resources` 目录中

## 打包为exe可执行文件

### 方法一：使用PyInstaller命令（推荐）

```bash
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --hidden-import=qdarkstyle --hidden-import=qdarkstyle.dark.palette --hidden-import=qdarkstyle.light.palette --add-data "ui;ui" --add-data "tools;tools" --add-data "resources;resources" --icon "resources/app_icon.ico" main.py
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
├── resources/           # 资源文件目录
│   ├── app_icon.ico     # 应用程序图标文件
│   └── README.md        # 资源文件说明
├── ui/                  # 界面模块
│   └── main_window.py   # 主窗口
├── tools/               # 工具模块
│   ├── base_tool.py     # 工具基类
│   ├── json_formatter.py# JSON格式化工具
│   ├── xml_formatter.py # XML格式化工具
│   ├── base64_converter.py # Base64转换工具
│   ├── name_converter.py# 命名转换工具
│   └── text_statistics.py# 文本统计工具
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

## 工具详细说明

### 文本统计工具
文本统计工具可以对输入的文本进行详细统计，包括：
- 总字数：文本中字符的总数
- 总字符数：文本中单词的总数
- 总汉字数：文本中汉字的数量
- 汉字符号：文本中中文标点符号的数量
- 外文字母：文本中英文字母的数量
- 外文单词：文本中英文单词的数量
- 外文符号：文本中英文标点符号的数量
- 数字：文本中数字字符的数量
- 字符长度：文本字符长度
- 字节大小：文本在UTF-8编码下的字节大小

## 注意事项

- 打包后的程序会生成一个文件夹，包含exe文件和依赖文件
- 如需单独的exe文件（无文件夹），可使用 `--onefile` 参数替换 `--onedir`
- 打包为单个exe文件启动较慢，但分发更简单
- 图标文件必须是ICO格式才能在Windows上正确显示