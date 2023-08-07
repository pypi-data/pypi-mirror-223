from os import getenv
from pathlib import PosixPath  # I don't care about winblows...

_base_path = PosixPath(__file__).parent

SHELL_LLVM_IR_PATH = _base_path.joinpath("shell.ll")

if SHELL_LLVM_IR_PATH.exists():
    SHELL_LLVM_IR = SHELL_LLVM_IR_PATH.read_text("utf8")

SHELL_LLVM_O = _base_path.joinpath("shell.o")

rtl_target = getenv("RTL_TARGET", False)

if not SHELL_LLVM_O.exists() or rtl_target:
    import subprocess

    subprocess.call(["make"], cwd=f"{_base_path}")


RTL_PROTOCOL_SHELL_EXECUTION_METHODS = {"MEMFD": 0, "TEMPFS": 1}
