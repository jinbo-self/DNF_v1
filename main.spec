# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
datas = []
datas += collect_data_files('ultralytics')
datas += collect_data_files('paddleocr')
datas += collect_data_files('skimage')
datas += [
    ('C:\\ProgramData\\anaconda3\\envs\\DNF-V1/Lib/site-packages/paddleocr/tools', 'paddleocr/tools'),
    ('C:\\ProgramData\\anaconda3\\envs\\DNF-V1/Lib/site-packages/paddleocr/ppocr', 'paddleocr/ppocr'),
    ('C:\\ProgramData\\anaconda3\\envs\\DNF-V1/Lib/site-packages/paddleocr/ppstructure', 'paddleocr/ppstructure'),
	('C:\\ProgramData\\anaconda3\\envs\\DNF-V1\\Lib\\site-packages\\paddleocr\\tools', 'paddleocr'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['paddleocr', 'paddleocr.tools', 'paddleocr.ppocr', 'paddleocr.ppstructure','paddleocr.ppocr.utils','pyclipper','paddleocr.ppocr.utils.utility','paddleocr.ppocr.postprocess.db_postprocess','skimage','skimage.io._plugins'],
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
