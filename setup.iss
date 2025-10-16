[Setup]
AppName=DevUtilsApp
AppVersion=1.0
AppPublisher=YourCompany
AppPublisherURL=https://your-website.com
AppSupportURL=https://your-website.com/support
AppUpdatesURL=https://your-website.com/updates
DefaultDirName={pf}\DevUtilsApp
DefaultGroupName=DevUtilsApp
OutputDir=D:\work\python\dev-util-app\installer
OutputBaseFilename=DevUtilsApp_Setup
SetupIconFile=D:\work\python\dev-util-app\assets\app_icon.ico
Compression=lzma
SolidCompression=yes
ShowTasksTreeLines=no
[Files]
Source: "D:\work\python\dev-util-app\dist\devUtilApp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\work\python\dev-util-app\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\DevUtilsApp"; Filename: "{app}\devUtilApp.exe"; IconFilename: "{app}\assets\app_icon.ico"
Name: "{commondesktop}\DevUtilsApp"; Filename: "{app}\devUtilApp.exe"; IconFilename: "{app}\assets\app_icon.ico"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Additional tasks"
Name: "launchprogram"; Description: "Run DevUtilsApp after installation"; GroupDescription: "Additional tasks"
[Run]
Filename: "{app}\devUtilApp.exe"; Description: "Run DevUtilsApp"; Flags: nowait postinstall skipifsilent; Tasks: launchprogram
