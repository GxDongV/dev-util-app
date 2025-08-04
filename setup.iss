[Setup]
AppName=DevUtilsApp
AppVersion=1.0
AppPublisher=YourCompany
AppPublisherURL=https://your-website.com
AppSupportURL=https://your-website.com/support
AppUpdatesURL=https://your-website.com/updates
DefaultDirName={pf}\DevUtilsApp
DefaultGroupName=DevUtilsApp
OutputDir=D:\work\python\devUtilsApp\installer
OutputBaseFilename=DevUtilsApp_Setup
SetupIconFile=D:\work\python\devUtilsApp\assets\app_icon.ico
Compression=lzma
SolidCompression=yes
[Files]
Source: "D:\work\python\devUtilsApp\dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\work\python\devUtilsApp\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\DevUtilsApp"; Filename: "{app}\main.exe"; IconFilename: "{app}\assets\app_icon.ico"
Name: "{commondesktop}\DevUtilsApp"; Filename: "{app}\main.exe"; IconFilename: "{app}\assets\app_icon.ico"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Additional tasks"; Flags: unchecked
[Run]
Filename: "{app}\main.exe"; Description: "Run DevUtilsApp"; Flags: nowait postinstall skipifsilent
