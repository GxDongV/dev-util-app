OutFile '../installer\DevUtilsApp_Setup.exe'
InstallDir '$PROGRAMFILES\DevUtilsApp'
Page Directory
Page InstFiles
Section 'MainSection' SEC01
  SetOutPath '$INSTDIR'
  File 'D:\work\python\devUtilsApp\dist\main.exe'
  CreateDirectory '$INSTDIR\assets'
  SetOutPath '$INSTDIR\assets'
  File /r 'D:\work\python\devUtilsApp\assets\*.*'
SectionEnd
Section 'Create Desktop Shortcut' SEC02
  CreateShortcut '$DESKTOP\DevUtilsApp.lnk' '$INSTDIR\main.exe' '' '$INSTDIR\assets\app_icon.ico'
SectionEnd
