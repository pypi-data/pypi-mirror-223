from os import getenv
from pathlib import PosixPath  # I don't care about winblows...

_base_path = PosixPath(__file__).parent

COMMON_LLVM_IR_PATH = _base_path.joinpath("rtl_common.ll")

if COMMON_LLVM_IR_PATH.exists():
    COMMON_LLVM_IR = COMMON_LLVM_IR_PATH.read_text("utf8")

COMMON_LLVM_O = _base_path.joinpath("rtl_common.o")

rtl_target = getenv("RTL_TARGET", False)

if not COMMON_LLVM_O.exists() or rtl_target:
    import subprocess

    subprocess.call(["make"], cwd=f"{_base_path}")