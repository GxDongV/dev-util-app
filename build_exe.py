import os
import sys
import subprocess

def build_exe():
    """
    使用PyInstaller将项目打包为exe可执行文件
    """
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    #         "--onedir",              # 打包成文件夹形式
    #         "--onefile",              # 打包成单文件形式
    # 构建命令
    cmd = [
        "pyinstaller",
        "--noconfirm",           # 不需要确认
        "--onefile",              # 打包成单文件形式
        "--windowed",            # 窗口模式，不显示控制台
        "--hidden-import=qdarkstyle", # 隐藏导入的模块
        "--hidden-import=qdarkstyle.dark.palette",  # 添加qdarkstyle.dark.palette模块
        "--hidden-import=qdarkstyle.light.palette",
        "--add-data", "ui;ui",   # 添加ui目录
        "--add-data", "tools;tools",  # 添加tools目录
        "main.py"
    ]
    
    print("开始打包项目...")
    print("执行命令:", " ".join(cmd))
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, cwd=current_dir, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        print("打包成功完成！")
        print("可执行文件位置: dist/main/main.exe")
        return True
    except subprocess.CalledProcessError as e:
        print("打包失败:")
        print("错误输出:", e.stderr)
        return False
    except FileNotFoundError:
        print("错误: 未找到pyinstaller命令，请确保已安装PyInstaller")
        print("安装命令: pip install pyinstaller")
        return False

if __name__ == "__main__":
    build_exe()