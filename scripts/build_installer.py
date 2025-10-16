import os
import shutil
import subprocess
import winreg  # 用于Windows注册表查询


def build_exe(onefile=True):
    """
    使用PyInstaller将项目打包
    onefile: True表示单文件打包，False表示多文件打包
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    dist_dir = os.path.join(project_root, 'dist')
    build_dir = os.path.join(project_root, 'build')
    spec_file = os.path.join(project_root, 'devUtilApp.spec')

    # 清理旧的构建文件
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(spec_file):
        os.remove(spec_file)

    # 构建PyInstaller命令

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
        "--name", "devUtilApp",  # 设置输出文件名为devUtilApp
        f"{os.path.join(project_root, 'src', 'main.py')}"
    ]

    # 根据参数决定是否使用单文件模式
    if onefile:
        cmd.append("--onefile")  # 单文件打包

    print("开始打包...")
    print("执行命令:", " ".join(cmd))

    try:
        result = subprocess.run(cmd, cwd=project_root, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        print("打包成功!")
        print(f"可执行文件位置: {os.path.join(dist_dir, 'devUtilApp.exe') if onefile else os.path.join(dist_dir, 'devUtilApp', 'devUtilApp.exe')}")
        return True
    except subprocess.CalledProcessError as e:
        print("打包失败:")
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
        exe_path = os.path.join(dist_dir, 'devUtilApp.exe')
    else:
        exe_path = os.path.join(dist_dir, 'devUtilApp', 'devUtilApp.exe')
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
            # 确保在安装完成页面显示选项框
            f.write(f"ShowTasksTreeLines=no\n")
            f.write(f"[Files]\n")
            if onefile:
                f.write(f"Source: \"{exe_path}\"; DestDir: \"{{app}}\"; Flags: ignoreversion\n")
                # 复制assets文件夹
                f.write(f"Source: \"{os.path.join(project_root, 'assets')}\\*\"; DestDir: \"{{app}}\\assets\"; Flags: ignoreversion recursesubdirs createallsubdirs\n")
            else:
                # 多文件模式需要复制整个目录
                f.write(f"Source: \"{os.path.join(dist_dir, 'devUtilApp')}\\*\"; DestDir: \"{{app}}\"; Flags: ignoreversion recursesubdirs createallsubdirs\n")
                # 复制assets文件夹
                f.write(f"Source: \"{os.path.join(project_root, 'assets')}\\*\"; DestDir: \"{{app}}\\assets\"; Flags: ignoreversion recursesubdirs createallsubdirs\n")
            
            # 图标设置（无论单文件还是多文件模式都需要）
            f.write(f"[Icons]\n")
            f.write(f"Name: \"{{group}}\\DevUtilsApp\"; Filename: \"{{app}}\\devUtilApp.exe\"; IconFilename: \"{{app}}\\assets\\app_icon.ico\"\n")
            f.write(f"Name: \"{{commondesktop}}\\DevUtilsApp\"; Filename: \"{{app}}\\devUtilApp.exe\"; IconFilename: \"{{app}}\\assets\\app_icon.ico\"; Tasks: desktopicon\n")
            
            # 任务设置 - 添加桌面快捷方式和运行软件选项
            f.write(f"[Tasks]\n")
            f.write(f"Name: \"desktopicon\"; Description: \"Create desktop shortcut\"; GroupDescription: \"Additional tasks\"\n")
            f.write(f"Name: \"launchprogram\"; Description: \"Run DevUtilsApp after installation\"; GroupDescription: \"Additional tasks\"\n")
            
            # 运行程序设置，与launchprogram任务关联
            f.write(f"[Run]\n")
            f.write(f"Filename: \"{{app}}\\devUtilApp.exe\"; Description: \"Run DevUtilsApp\"; Flags: nowait postinstall skipifsilent; Tasks: launchprogram\n")

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
            # 包含所需的NSIS库以支持任务页面
            f.write("!include MUI2.nsh\n")
            
            # 定义安装程序属性
            output_file = os.path.join(installer_output_dir, 'DevUtilsApp_Setup.exe')
            f.write(f"OutFile '{output_file.replace('/', '\\')}'\n")
            f.write("InstallDir '$PROGRAMFILES\\DevUtilsApp'\n")
            
            # 设置安装程序页面
            f.write("!insertmacro MUI_PAGE_DIRECTORY\n")
            f.write("!insertmacro MUI_PAGE_INSTFILES\n")
            
            # 定义完成页面并启用自定义任务
            f.write("!define MUI_FINISHPAGE_RUN '$INSTDIR\\devUtilApp.exe'\n")

            f.write("!define MUI_FINISHPAGE_SHOWREADME_CHECKED false\n")
            f.write("!define MUI_FINISHPAGE_RUN_CHECKED true\n")
            f.write("!define MUI_FINISHPAGE_RUN_TEXT 'Run DevUtilsApp'\n")
            f.write("!insertmacro MUI_PAGE_FINISH\n")
            
            # 语言设置
            f.write("!insertmacro MUI_LANGUAGE 'English'\n")
            
            # 定义安装部分
            f.write("Section 'MainSection' SEC01\n")
            f.write(f"  SetOutPath '$INSTDIR'\n")
            if onefile:
                f.write(f"  File '{exe_path}'\n")
            else:
                # 多文件模式需要复制整个目录
                f.write(f"  SetOutPath '$INSTDIR'\n")
                f.write(f"  File /r '{os.path.join(dist_dir, 'devUtilApp')}\\*.*'\n")
            # 复制assets文件夹
            f.write(f"  CreateDirectory '$INSTDIR\\assets'\n")
            f.write(f"  SetOutPath '$INSTDIR\\assets'\n")
            f.write(f"  File /r '{os.path.join(project_root, 'assets')}\\*.*'\n")
            
            # 创建空的README文件以避免错误
            f.write("  FileOpen $0 '$INSTDIR\\README.txt' w\n")
            f.write("  FileClose $0\n")
            
            # 创建开始菜单快捷方式
            f.write("  CreateDirectory '$SMPROGRAMS\\DevUtilsApp'\n")
            f.write("  CreateShortcut '$SMPROGRAMS\\DevUtilsApp\\DevUtilsApp.lnk' '$INSTDIR\\devUtilApp.exe' '' '$INSTDIR\\assets\\app_icon.ico'\n")
            f.write("SectionEnd\n")
            
            # 创建桌面快捷方式部分（默认选中）
            f.write("Var DesktopShortcut\n")
            f.write("Function .onInit\n")
            f.write("  StrCpy $DesktopShortcut 1\n")
            f.write("FunctionEnd\n")
            
            # 添加自定义页面用于桌面快捷方式选项
            f.write("Page custom CreateShortcutPage\n")
            f.write("Function CreateShortcutPage\n")
            f.write("  nsDialogs::Create 1018\n")
            f.write("  Pop $0\n")
            
            # 创建标签
            f.write("  ${NSD_CreateLabel} 0 0 100% 12u 'Select additional tasks:'\n")
            f.write("  Pop $0\n")
            
            # 创建桌面快捷方式复选框（默认选中）
            f.write("  ${NSD_CreateCheckBox} 0 24u 100% 12u 'Create desktop shortcut'\n")
            f.write("  Pop $0\n")
            f.write("  ${If} $DesktopShortcut == 1\n")
            f.write("    ${NSD_Check} $0\n")
            f.write("  ${EndIf}\n")
            f.write("  ${NSD_OnClick} $0 OnDesktopShortcutClick\n")
            
            f.write("  nsDialogs::Show\n")
            f.write("FunctionEnd\n")
            
            f.write("Function OnDesktopShortcutClick\n")
            f.write("  ${NSD_GetState} $0 $DesktopShortcut\n")
            f.write("FunctionEnd\n")
            
            # 安装完成后的回调
            f.write("Function .onInstSuccess\n")
            f.write("  ${If} $DesktopShortcut == 1\n")
            f.write("    CreateShortcut '$DESKTOP\\DevUtilsApp.lnk' '$INSTDIR\\devUtilApp.exe' '' '$INSTDIR\\assets\\app_icon.ico'\n")
            f.write("  ${EndIf}\n")
            f.write("FunctionEnd\n")

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
    # 使用一站式构建函数创建安装包（默认使用Inno Setup）
    # 如需使用NSIS，可修改为build_with_installer("nsis", build_exe_first=True, onefile=True)
    build_with_installer("inno", build_exe_first=True, onefile=True)
