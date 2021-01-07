# -*- mode: python ; coding: utf-8 -*-

# https://github.com/pyinstaller/pyinstaller/issues/4064#issuecomment-471063543
import distutils
if (getattr(distutils, 'distutils_path', None) != None) and distutils.distutils_path.endswith('__init__.py'):
    distutils.distutils_path = os.path.dirname(distutils.distutils_path)

block_cipher = None
excluded_modules = ['torch.distributions'] # <<< ADD THIS LINE

a = Analysis(['ui.py'],
             pathex=[''],
             binaries=[],
             datas=[('D:/ProgramFiles/anaconda3/envs/test2/Lib/site-packages/matplotlib/mpl-data/matplotlibrc', './matplotlib/mpl-data/')],
             hiddenimports=['torch.distributions','scipy.spatial.transform._rotation_groups', 'numpy.random.common','numpy.random.bounded_integers', 'numpy.random.entropy', 'fastprogress'],
             hookspath=['hooks'],
             runtime_hooks=[],
             excludes=excluded_modules,    # <<< CHANGE THIS LINE
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
