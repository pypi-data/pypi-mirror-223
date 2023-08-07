from os import getenv
from pathlib import PosixPath  # I don't care about winblows...

_base_path = PosixPath(__file__).parent

XOR_LLVM_IR_PATH = _base_path.joinpath("xor.ll")

if XOR_LLVM_IR_PATH.exists():
    XOR_LLVM_IR = XOR_LLVM_IR_PATH.read_text("utf8")

XOR_LLVM_O = _base_path.joinpath("xor.o")

rtl_target = getenv("RTL_TARGET", False)

if not XOR_LLVM_O.exists() or rtl_target:
    import subprocess

    subprocess.call(["make"], cwd=f"{_base_path}")
