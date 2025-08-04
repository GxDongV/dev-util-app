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
