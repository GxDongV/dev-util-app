import os
import sys
import os
import subprocess
import shutil
import winreg  # 用于Windows注册表查询
from pathlib import Path

def build_exe(onefile=True):
    """
    使用PyInstaller将项目打包
    onefile: True表示单文件打包，False表示多文件打包
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    dist_dir = os.path.join(project_root, 'dist')
    build_dir = os.path.join(project_root, 'build')
    spec_file = os.path.join(project_root, 'main.spec')

    # 清理旧的构建文件
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(spec_file):
        os.remove(spec_file)

    # 构建PyInstaller命令
    # 获取项目根目录
    project_root = os.path.abspath(os.path.join(current_dir, '..'))

    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--windowed",          # 窗口模式
        "--hidden-import=qdarkstyle",
        "--hidden-import=qdarkstyle.dark.palette",
        "--hidden-import=qdarkstyle.light.palette",
        "--hidden-import=qdarkstyle.dark.stylesheet",
        "--hidden-import=qdarkstyle.light.stylesheet",
        "--hidden-import=qdarkstyle.utils",
        "--add-data", f"{os.path.join(project_root, 'ui')};ui",
        "--add-data", f"{os.path.join(project_root, 'tools')};tools",
        "--add-data", f"{os.path.join(project_root, 'assets')};assets",
        "--icon", f"{os.path.join(project_root, 'assets', 'app_icon.ico')}",
        f"{os.path.join(project_root, 'src', 'main.py')}"
    ]

    # 根据参数决定是否使用单文件模式
    if onefile:
        cmd.append("--onefile")  # 单文件打包
    else:
        # 多文件模式下，可以指定输出目录名称
        cmd.extend(["--name", "main"])  # 设置输出文件名

    print("开始单文件打包...")
    print("执行命令:", " ".join(cmd))

    try:
        result = subprocess.run(cmd, cwd=project_root, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        print("单文件打包成功!")
        print(f"可执行文件位置: {os.path.join(dist_dir, 'main.exe') if onefile else os.path.join(dist_dir, 'main', 'main.exe')}")
        return True
    except subprocess.CalledProcessError as e:
        print("单文件打包失败:")
        print("错误输出:", e.stderr)
        return False
    except FileNotFoundError:
        print("错误: 未找到pyinstaller命令，请确保已安装PyInstaller")
        print("安装命令: pip install pyinstaller")
        return False

def find_inno_setup():
    """
    查找Inno Setup的安装路径
    返回ISCC.exe的完整路径，如果未找到则返回None
    """
    # 尝试直接运行命令（检查是否在PATH中）
    try:
        subprocess.run(["ISCC.exe", "/?"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "ISCC.exe"
    except FileNotFoundError:
        pass

    # 从注册表查找
    try:
        # 检查32位注册表
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1")
        install_location = winreg.QueryValueEx(key, "InstallLocation")[0]
        winreg.CloseKey(key)
        return os.path.join(install_location, "ISCC.exe")
    except (OSError, FileNotFoundError):
        pass

    # 检查64位注册表
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1")
        install_location = winreg.QueryValueEx(key, "InstallLocation")[0]
        winreg.CloseKey(key)
        return os.path.join(install_location, "ISCC.exe")
    except (OSError, FileNotFoundError):
        pass

    # 常见安装路径
    common_paths = [
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    return None

def find_nsis():
    """
    查找NSIS的安装路径
    返回makensis.exe的完整路径，如果未找到则返回None
    """
    # 尝试直接运行命令（检查是否在PATH中）
    try:
        subprocess.run(["makensis.exe", "/?"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "makensis.exe"
    except FileNotFoundError:
        pass

    # 从注册表查找
    try:
        # 检查32位注册表
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\NSIS")
        install_location = winreg.QueryValueEx(key, "Install Location")[0]
        winreg.CloseKey(key)
        return os.path.join(install_location, "makensis.exe")
    except (OSError, FileNotFoundError):
        pass

    # 检查64位注册表
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\NSIS")
        install_location = winreg.QueryValueEx(key, "Install Location")[0]
        winreg.CloseKey(key)
        return os.path.join(install_location, "makensis.exe")
    except (OSError, FileNotFoundError):
        pass

    # 常见安装路径
    common_paths = [
        r"C:\Program Files\NSIS\makensis.exe",
        r"C:\Program Files (x86)\NSIS\makensis.exe",
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    return None

def create_installer(installer_tool="inno", onefile=True):
    """
    创建安装包
    installer_tool: 可选 'inno' 或 'nsis'
    onefile: True表示使用单文件exe，False表示使用多文件目录
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    dist_dir = os.path.join(project_root, 'dist')
    if onefile:
        exe_path = os.path.join(dist_dir, 'main.exe')
    else:
        exe_path = os.path.join(dist_dir, 'main', 'main.exe')
    installer_output_dir = os.path.join(project_root, 'installer')

    # 检查单文件是否存在
    if not os.path.exists(exe_path):
        print(f"错误: 未找到单文件exe: {exe_path}")
        print("请先运行build_exe()成功后再创建安装包")
        return False

    # 创建安装包输出目录
    if not os.path.exists(installer_output_dir):
        os.makedirs(installer_output_dir)

    if installer_tool.lower() == "inno":
        # 使用Inno Setup创建安装包
        print("使用Inno Setup创建安装包...")
        # 查找Inno Setup
        inno_path = find_inno_setup()
        if not inno_path:
            print("错误: 未找到Inno Setup，请先安装")
            print("下载地址: http://www.jrsoftware.org/isdl.php")
            return False
        print(f"检测到Inno Setup: {inno_path}")

        # 创建Inno Setup脚本
        inno_script = os.path.join(current_dir, '..', 'setup.iss')
        with open(inno_script, 'w', encoding='utf-8') as f:
            f.write(f"[Setup]\n")
            f.write(f"AppName=DevUtilsApp\n")
            f.write(f"AppVersion=1.0\n")
            f.write(f"AppPublisher=YourCompany\n")
            f.write(f"AppPublisherURL=https://your-website.com\n")
            f.write(f"AppSupportURL=https://your-website.com/support\n")
            f.write(f"AppUpdatesURL=https://your-website.com/updates\n")
            f.write(f"DefaultDirName={{pf}}\\DevUtilsApp\n")
            f.write(f"DefaultGroupName=DevUtilsApp\n")
            f.write(f"OutputDir={installer_output_dir}\n")
            f.write(f"OutputBaseFilename=DevUtilsApp_Setup\n")
            f.write(f"SetupIconFile={os.path.join(project_root, 'assets', 'app_icon.ico')}\n")
            f.write(f"Compression=lzma\n")
            f.write(f"SolidCompression=yes\n")
            f.write(f"[Files]\n")
            if onefile:
                f.write(f"Source: \"{exe_path}\"; DestDir: \"{{app}}\"; Flags: ignoreversion\n")
            else:
                # 多文件模式需要复制整个目录
                f.write(f"Source: \"{os.path.join(dist_dir, 'main')}\*\"; DestDir: \"{{app}}\"; Flags: ignoreversion recursesubdirs createallsubdirs\n")
            f.write(f"[Icons]\n")
            f.write(f"Name: \"{{group}}\\DevUtilsApp\"; Filename: \"{{app}}\\main.exe\"; IconFilename: \"{{app}}\\assets\\app_icon.ico\"\n")
            f.write(f"Name: \"{{commondesktop}}\\DevUtilsApp\"; Filename: \"{{app}}\\main.exe\"; IconFilename: \"{{app}}\\assets\\app_icon.ico\"; Tasks: desktopicon\n")
            f.write(f"[Tasks]\n")
            f.write(f"Name: \"desktopicon\"; Description: \"Create desktop shortcut\"; GroupDescription: \"Additional tasks\"; Flags: unchecked\n")
            f.write(f"[Run]\n")
            f.write(f"Filename: \"{{app}}\\main.exe\"; Description: \"Run DevUtilsApp\"; Flags: nowait postinstall skipifsilent\n")

        # 运行Inno Setup编译脚本
        try:
            cmd = [inno_path, inno_script]
            result = subprocess.run(cmd, cwd=current_dir, check=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True)
            print(f"安装包创建成功: {os.path.join(installer_output_dir, 'DevUtilsApp_Setup.exe')}")
            return True
        except subprocess.CalledProcessError as e:
            print("安装包创建失败:")
            print("错误输出:", e.stderr)
            return False
    elif installer_tool.lower() == "nsis":
        # 使用NSIS创建安装包
        print("使用NSIS创建安装包...")
        # 查找NSIS
        nsis_path = find_nsis()
        if not nsis_path:
            print("错误: 未找到NSIS，请先安装")
            print("下载地址: https://nsis.sourceforge.io/Download")
            return False
        print(f"检测到NSIS: {nsis_path}")

        # 创建NSIS脚本
        nsis_script = os.path.join(current_dir, '..', 'setup.nsi')
        with open(nsis_script, 'w', encoding='utf-8') as f:
            f.write("OutFile '../installer\\DevUtilsApp_Setup.exe'\n")
            f.write("InstallDir '$PROGRAMFILES\\DevUtilsApp'\n")
            f.write("Page Directory\n")
            f.write("Page InstFiles\n")
            f.write("Section 'MainSection' SEC01\n")
            f.write(f"  SetOutPath '$INSTDIR'\n")
            if onefile:
                f.write(f"  File '{exe_path}'\n")
            else:
                # 多文件模式需要复制整个目录
                f.write(f"  SetOutPath '$INSTDIR'\n")
                f.write(f"  File /r '{os.path.join(dist_dir, 'main')}\\*.*'\n")
            f.write(f"  File '{os.path.join(project_root, 'assets', 'app_icon.ico')}'\n")
            f.write("SectionEnd\n")
            f.write("Section 'Create Desktop Shortcut' SEC02\n")
            f.write("  CreateShortcut '$DESKTOP\\DevUtilsApp.lnk' '$INSTDIR\\main.exe' '' '$INSTDIR\\app_icon.ico'\n")
            f.write("SectionEnd\n")

        # 运行NSIS编译脚本
        try:
            cmd = [nsis_path, nsis_script]
            result = subprocess.run(cmd, cwd=current_dir, check=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True)
            print(f"安装包创建成功: {os.path.join(installer_output_dir, 'DevUtilsApp_Setup.exe')}")
            return True
        except subprocess.CalledProcessError as e:
            print("安装包创建失败:")
            print("错误输出:", e.stderr)
            return False
    else:
        print(f"错误: 不支持的安装包工具: {installer_tool}")
        print("支持的工具: 'inno', 'nsis'")
        return False

def build_with_installer(installer_tool="inno", build_exe_first=True, onefile=True):
    """
    一站式构建exe并创建安装包
    build_exe_first: 是否先构建exe
    onefile: True表示单文件打包，False表示多文件打包
    """
    if build_exe_first:
        if not build_exe(onefile):
            return False
    return create_installer(installer_tool, onefile)

if __name__ == "__main__":
    # 测试工具路径检测
    #test_installer_tools()
    
    # 构建单文件exe
    build_exe(onefile=True)
    
    # 创建安装包，使用NSIS
    create_installer(installer_tool="nsis", onefile=True)
    # 默认为Inno Setup，也可以指定为'nsis'
    # 如需禁用先构建exe，可设置build_exe_first=False
    build_with_installer("inno", build_exe_first=True, onefile=True)
