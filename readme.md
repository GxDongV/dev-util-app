# devUtilApp

一个实用的开发工具集合，提供JSON格式化、XML格式化等功能，基于PyQt5构建图形界面。

## 功能特点
- JSON数据格式化与验证
- XML数据格式化与验证
- 可扩展的工具架构
- 简洁直观的图形界面

## 项目结构
```
devUtilApp/
├── main.py                  # 主程序入口
├── requirements.txt         # 项目依赖
├── tools/                   # 工具模块
│   ├── __init__.py
│   ├── base_tool.py         # 工具基类
│   ├── json_format.py       # JSON格式化工具
│   └── xml_format.py        # XML格式化工具
└── ui/
    └── main_window.py       # 主窗口UI
```

## 环境要求
- Python 3.8+
- PyQt5 5.15.7

## 安装步骤
1. 克隆或下载项目到本地
2. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```
Pip install qdarkstyle
## 使用方法
运行主程序：
```
python main.py
```

## 扩展开发
如需添加新工具，只需继承`tools.base_tool.BaseTool`类并实现相应方法即可。
