import platform

if platform.system() != 'Windows':
    print("\n**** This can be run only on Windows! ****")
    print("     exiting with error.\n\n")
    exit(1)

import cx_Freeze

# example from: 
# https://stackoverflow.com/questions/54210392/how-can-i-convert-pygame-to-exe
# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable('main.py', base = "Win32GUI")]

cx_Freeze.setup(
    name = "Pirate",
    options = {"build_exe" : 
        {
            "packages" : ["pygame"], 
            "include_files" : ['audio/', 'graphics/', 'levels/']
            }
        },
    executables = executables
)
