from cx_Freeze import setup, Executable

setup(
    name="EPSImester",
    version="0.1",
    description="EPSImester!",
    executables=[Executable("main.py")]
)
