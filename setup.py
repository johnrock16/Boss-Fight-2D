import sys
from cx_Freeze import setup, Executable
import pygame
from random import randint



base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("Jogo.py", base=base)
]

buildOptions = dict(
        packages = [],
        includes = ["pygame","random"],
        include_files = ["./imagens","./musicas","./efeitos-sonoros"],
        excludes = []
)




setup(
    name = "VouMatarMano",
    version = "1.0",
    description = "Descrição do programa",
    options = dict(build_exe = buildOptions),
    executables = executables
 )