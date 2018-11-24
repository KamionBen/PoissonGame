# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py', 'main.spec'],
             pathex=['/Users/jamin/PycharmProjects/PoissonGame'],
             binaries=[],
             datas=[('/Users/jamin/PycharmProjects/PoissonGame/font/', 'font'),
                    ('/Users/jamin/PycharmProjects/PoissonGame/img720/', 'img720')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PoissonGame',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
app = BUNDLE(coll,
             name='PoissonGame.app',
             icon=None,
             bundle_identifier=None)
