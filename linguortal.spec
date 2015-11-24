# -*- mode: python -*-
a = Analysis(['linguortal.py'],
             pathex=['C:\\Users\\jmickle\\Documents\\GitHub\\linguortal-gen'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='linguortal.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
