# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['school_voting.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('elections/*', 'elections'),
        ('photos/*', 'photos'),
        ('symbols/*', 'symbols')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SchoolVoting',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False
    # Remove this line: cipher=block_cipher,
)