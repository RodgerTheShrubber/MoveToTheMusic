from distutils.core import setup
import py2exe

setup (console =["GameController.py"],
       py_modules = ['GameSettings'],
       options={"py2exe": {"compressed": 1,
                           "optimize": 2,
                           "dist_dir": "../dist",
                           #'typelibs': [('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 0, 5, 0)],
                           'packages': ['encodings'],
                           'bundle_files':1,
                           }}

)
