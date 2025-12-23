# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

block_cipher = None
qml_path = Path('src/qml')

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[(str(qml_path), 'qml')],
    hiddenimports=[
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuickControls2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='tuda-suda',
    debug=False,
    strip=False,
    upx=True,
    console=False,
)

