import sys
import os
# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
from build_installer import build_exe, create_installer, build_with_installer

def build_single_file():
    """
    构建单文件模式的可执行文件
    """
    print("开始构建单文件模式可执行文件...")
    success = build_exe(onefile=True)
    if success:
        print("单文件模式可执行文件构建成功!")
        print(f"可执行文件位置: {os.path.join(current_dir, '..', 'dist', 'devUtilApp.exe')}")
    else:
        print("单文件模式可执行文件构建失败!")
    return success

def build_multi_file():
    """
    构建多文件模式的可执行文件
    """
    print("开始构建多文件模式可执行文件...")
    success = build_exe(onefile=False)
    if success:
        print("多文件模式可执行文件构建成功!")
        print(f"可执行文件目录: {os.path.join(current_dir, '..', 'dist', 'devUtilApp')}")
    else:
        print("多文件模式可执行文件构建失败!")
    return success

def build_inno_setup_installer():
    """
    使用Inno Setup构建安装包
    """
    print("开始使用Inno Setup构建安装包...")
    
    # 先构建多文件可执行文件
    print("首先构建多文件可执行文件...")
    if not build_exe(onefile=False):
        print("安装包构建失败：多文件构建失败")
        return False
    
    # 创建安装包
    success = create_installer(installer_tool="inno", onefile=False)
    if success:
        print("Inno Setup安装包构建成功!")
    else:
        print("Inno Setup安装包构建失败!")
    return success

def build_nsis_installer():
    """
    使用NSIS构建安装包
    """
    print("开始使用NSIS构建安装包...")
    
    # 先构建多文件可执行文件
    print("首先构建多文件可执行文件...")
    if not build_exe(onefile=False):
        print("安装包构建失败：多文件构建失败")
        return False
    
    # 创建安装包
    success = create_installer(installer_tool="nsis", onefile=False)
    if success:
        print("NSIS安装包构建成功!")
    else:
        print("NSIS安装包构建失败!")
    return success

if __name__ == "__main__":
    print("=== DevUtilsApp 打包工具 ===")
    print("1. 构建单文件可执行文件")
    print("2. 构建多文件可执行文件")
    print("3. 使用Inno Setup构建安装包")
    print("4. 使用NSIS构建安装包")
    
    choice = input("请选择打包方式 (1-4): ")
    
    if choice == '1':
        build_single_file()
    elif choice == '2':
        build_multi_file()
    elif choice == '3':
        build_inno_setup_installer()
    elif choice == '4':
        build_nsis_installer()
    else:
        print("无效的选择，请输入 1、2、3 或 4")
    
    print("\n打包工具执行完毕")