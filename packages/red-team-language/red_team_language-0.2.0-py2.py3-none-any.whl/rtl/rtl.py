import shlex

from argparse import ArgumentParser
from pathlib import PosixPath

from rtl.parser.driver import Driver

CURRENT_PATH = PosixPath(__file__).parent


def main():
    parser = ArgumentParser(
        "rtl",
        None,
        "The Red-Team-Language compiler enables one to write scripts and deploy them as static executables - for the lolz of course!",
        add_help=True,
    )

    parser.add_argument(
        "--src",
        action="store",
        help="The source *.rtl script to compile to LLVM-IR",
        required=True,
        type=PosixPath,
    )
    parser.add_argument(
        "--dst",
        action="store",
        help="The where to write the output (default is stdout)",
        required=False,
        type=PosixPath,
    )
    parser.add_argument(
        "--ir",
        action="store_true",
        help="Emit LLVM-IR",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--asm",
        action="store_true",
        help="Emit assembly for this machine",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--obj",
        action="store_true",
        help="Emit an object file for this machine",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Attempt to build a binary from the provided --src",
        required=False,
        default=False,
    )

    args = parser.parse_args()

    driver = Driver(args.src)

    if not args.build:
        if not args.ir and not args.asm and not args.obj:
            args.ir = True

        print(driver.emit(args))
    else:
        """
        The following is the silliest, shortsighted, sick, stultification of code ever seen; in short, stereoisomeric with shit...I'll fix it someday...
        """
        args.ir = False
        args.asm = True
        args.obj = False
        args.dst = PosixPath(__file__).parent.joinpath("a.s")

        fn = driver.emit(args)

        filename = f"{PosixPath('/tmp/').joinpath(PosixPath(f'{args.src}').stem)}.elf"

        import subprocess

        from rtl.lib.protocol.common import COMMON_LLVM_O
        from rtl.lib.protocol.shell import SHELL_LLVM_O
        from rtl.lib.protocol.ssh import SSH_LLVM_O
        from rtl.lib.transform.xor import XOR_LLVM_O

        llvm_ir_contents = str(driver.module)

        LLVM_O = f"{COMMON_LLVM_O}"
        INCLUDES = ""
        LIBRARY_PATHS = ""
        CFLAGS = "-fPIC"

        if ".shell" in llvm_ir_contents:
            LLVM_O += f" {SHELL_LLVM_O}"

        if ".ssh" in llvm_ir_contents:
            LLVM_O += f" {SSH_LLVM_O}"
            INCLUDES += f" -I{CURRENT_PATH}/lib/protocol/ssh/libssh2/include/"
            LIBRARY_PATHS += f" -L{CURRENT_PATH}/lib/protocol/ssh/libssh2/build/src"
            LIBRARY_PATHS += f" -L{CURRENT_PATH}/lib/protocol/ssh/mbedtls/build/library"
            # CFLAGS += " -Wl,-s"
            CFLAGS += " -lssh2"
            CFLAGS += " -lmbedtls"
            CFLAGS += " -lmbedcrypto"
            CFLAGS += " -lmbedx509"

        if ".xor" in llvm_ir_contents:
            LLVM_O += f" {XOR_LLVM_O}"

        print(LLVM_O)

        args = shlex.split(
            f"zig cc -g {INCLUDES} {LIBRARY_PATHS} -target {driver.rtl_target} {CFLAGS} {LLVM_O} {fn} -o {filename}"
        )

        if (
            subprocess.call(
                args,
                cwd=f"{PosixPath(__file__).parent}",
            )
            != 0
        ):
            print(
                "Failed to compile - is zig on PATH? build...is an experiment in how horrible one can write functional Python code xD"
            )
            exit(2)
        else:
            # subprocess.call(
            #     shlex.split(f"strip -s {filename}"),
            #     cwd=f"{PosixPath(__file__).parent}",
            # )
            print(f"done building {filename}")


if __name__ == "__main__":
    main()
