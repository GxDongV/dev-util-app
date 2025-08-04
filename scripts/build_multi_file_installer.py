import os
import sys
import os
# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
from build_installer import build_with_installer

if __name__ == "__main__":
    print("开始构建多文件模式安装包...")
    # 使用多文件模式构建Inno Setup安装包
    success = build_with_installer("inno", build_exe_first=True, onefile=False)
    if success:
        print("多文件模式安装包构建成功!")
        print(f"安装包位置: {os.path.join(current_dir, '..', 'installer', 'DevUtilsApp_Setup.exe')}")
    else:
        print("多文件模式安装包构建失败!")