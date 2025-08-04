import os
import sys

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 添加src目录到Python路径
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.append(src_dir)

# 运行主程序
try:
    import main
    print("成功启动DevUtilsApp...")
except ImportError as e:
    print(f"启动失败: 无法导入main模块 - {e}")
    print("请确保src目录下存在main.py文件")
    sys.exit(1)