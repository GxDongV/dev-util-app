OutFile 'installer\DevUtilsApp_Setup.exe'
InstallDir '$PROGRAMFILES\DevUtilsApp'
Page Directory
Page InstFiles
Section 'MainSection' SEC01
  SetOutPath '$INSTDIR'
  File 'D:\work\python\devUtilsApp\dist\main.exe'
  File 'D:\work\python\devUtilsApp\assets\app_icon.ico'
SectionEnd
Section 'Create Desktop Shortcut' SEC02
  CreateShortcut '$DESKTOP\DevUtilsApp.lnk' '$INSTDIR\main.exe' '' '$INSTDIR\app_icon.ico'
SectionEnd
