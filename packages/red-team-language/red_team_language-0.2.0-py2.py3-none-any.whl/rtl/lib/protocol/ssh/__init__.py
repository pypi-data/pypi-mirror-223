from os import getenv
from pathlib import PosixPath  # I don't care about winblows...

_base_path = PosixPath(__file__).parent

SSH_LLVM_IR_PATH = _base_path.joinpath("ssh.ll")

if SSH_LLVM_IR_PATH.exists():
    SSH_LLVM_IR = SSH_LLVM_IR_PATH.read_text("utf8")

SSH_LLVM_O = _base_path.joinpath("ssh.o")

rtl_target = getenv("RTL_TARGET", False)

if not SSH_LLVM_O.exists() or rtl_target:
    import subprocess

    subprocess.call(["make"], cwd=f"{_base_path}")
