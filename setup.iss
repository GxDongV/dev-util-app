#ifndef AppVersion
  #define AppVersion Trim(FileRead(FileOpen("VERSION")))
#endif
#ifndef SourceDir
  #define SourceDir "dist\portable\DevUtilsApp"
#endif
#ifndef ReleaseDir
  #define ReleaseDir "release"
#endif

[Setup]
AppId={{C2782961-2554-46F8-9E91-A9CF00C756F7}
AppName=DevUtilsApp
AppVersion={#AppVersion}
AppVerName=DevUtilsApp {#AppVersion}
AppPublisher=GxDongV
AppPublisherURL=https://github.com/GxDongV/dev-util-app
AppSupportURL=https://github.com/GxDongV/dev-util-app/issues
AppUpdatesURL=https://github.com/GxDongV/dev-util-app/releases
DefaultDirName={localappdata}\Programs\DevUtilsApp
DefaultGroupName=DevUtilsApp
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir={#ReleaseDir}
OutputBaseFilename=DevUtilsApp-{#AppVersion}-windows-x64-setup
SetupIconFile=assets\app_icon.ico
UninstallDisplayIcon={app}\DevUtilsApp.exe
LicenseFile=LICENSE
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
CloseApplications=yes

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Icons]
Name: "{group}\DevUtilsApp"; Filename: "{app}\DevUtilsApp.exe"
Name: "{userdesktop}\DevUtilsApp"; Filename: "{app}\DevUtilsApp.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\DevUtilsApp.exe"; Description: "Launch DevUtilsApp"; Flags: nowait postinstall skipifsilent
