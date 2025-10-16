!include MUI2.nsh
OutFile 'D:\work\python\dev-util-app\installer\DevUtilsApp_Setup.exe'
InstallDir '$PROGRAMFILES\DevUtilsApp'
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN '$INSTDIR\devUtilApp.exe'
!define MUI_FINISHPAGE_SHOWREADME_CHECKED false
!define MUI_FINISHPAGE_RUN_CHECKED true
!define MUI_FINISHPAGE_RUN_TEXT 'Run DevUtilsApp'
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE 'English'
Section 'MainSection' SEC01
  SetOutPath '$INSTDIR'
  SetOutPath '$INSTDIR'
  File /r 'D:\work\python\dev-util-app\dist\devUtilApp\*.*'
  CreateDirectory '$INSTDIR\assets'
  SetOutPath '$INSTDIR\assets'
  File /r 'D:\work\python\dev-util-app\assets\*.*'
  FileOpen $0 '$INSTDIR\README.txt' w
  FileClose $0
  CreateDirectory '$SMPROGRAMS\DevUtilsApp'
  CreateShortcut '$SMPROGRAMS\DevUtilsApp\DevUtilsApp.lnk' '$INSTDIR\devUtilApp.exe' '' '$INSTDIR\assets\app_icon.ico'
SectionEnd
Var DesktopShortcut
Function .onInit
  StrCpy $DesktopShortcut 1
FunctionEnd
Page custom CreateShortcutPage
Function CreateShortcutPage
  nsDialogs::Create 1018
  Pop $0
  ${NSD_CreateLabel} 0 0 100% 12u 'Select additional tasks:'
  Pop $0
  ${NSD_CreateCheckBox} 0 24u 100% 12u 'Create desktop shortcut'
  Pop $0
  ${If} $DesktopShortcut == 1
    ${NSD_Check} $0
  ${EndIf}
  ${NSD_OnClick} $0 OnDesktopShortcutClick
  nsDialogs::Show
FunctionEnd
Function OnDesktopShortcutClick
  ${NSD_GetState} $0 $DesktopShortcut
FunctionEnd
Function .onInstSuccess
  ${If} $DesktopShortcut == 1
    CreateShortcut '$DESKTOP\DevUtilsApp.lnk' '$INSTDIR\devUtilApp.exe' '' '$INSTDIR\assets\app_icon.ico'
  ${EndIf}
FunctionEnd
