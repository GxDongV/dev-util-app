# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\work\\python\\dev-util-app\\src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\work\\python\\dev-util-app\\ui', 'ui'), ('D:\\work\\python\\dev-util-app\\tools', 'tools'), ('D:\\work\\python\\dev-util-app\\assets', 'assets')],
    hiddenimports=['qdarkstyle', 'qdarkstyle.dark.palette', 'qdarkstyle.light.palette', 'qdarkstyle.dark.stylesheet', 'qdarkstyle.light.stylesheet', 'qdarkstyle.utils'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\work\\python\\dev-util-app\\assets\\app_icon.ico'],
)
