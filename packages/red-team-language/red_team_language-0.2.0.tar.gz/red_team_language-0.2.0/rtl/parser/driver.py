from os import getenv
from pathlib import PosixPath

import llvmlite.ir as llvmir
import llvmlite.binding as llvm
from rtl.lib import RTL_DEFAULT_TARGET, ZIGLANG_TARGETS

from rtl.parser.credential import Credential
from rtl.parser.host import Host
from rtl.parser.executable import Executable
from rtl.parser._with import With


class Driver:
    LINE_TRIGGER_MAP = {
        Credential.LINE_TRIGGER: Credential.parse,
        Host.LINE_TRIGGER: Host.parse,
        Executable.LINE_TRIGGER: Executable.parse,
        With.LINE_TRIGGER: With.parse,
    }
    LINE_TRIGGERS = LINE_TRIGGER_MAP.keys()

    def __init__(self, filepath):
        self.rtl_target = getenv("RTL_TARGET", RTL_DEFAULT_TARGET)

        if self.rtl_target not in ZIGLANG_TARGETS:
            print(f"Unsupported target: {self.rtl_target}")
            exit(1)

        llvm.initialize()
        llvm.initialize_all_asmprinters()
        llvm.initialize_all_targets()
        # llvm.initialize_native_target()
        # llvm.initialize_native_asmprinter()

        self.module = llvmir.Module("RTL")
        self.filepath = PosixPath(filepath).expanduser().resolve()

        if not self.filepath.exists():
            raise FileNotFoundError()

        self.script = []
        self.__llvm_module = ""

        self._parse()
        self._build()

    def _parse(self):
        with open(self.filepath, "r") as fh:
            line = True

            while line:
                line = fh.readline()

                tokens = line.strip().split(" ")

                if tokens[0].startswith("#"):
                    continue

                for trigger_key in self.LINE_TRIGGERS:
                    if trigger_key == tokens[0]:
                        self.script.append(self.LINE_TRIGGER_MAP[trigger_key](tokens, fh))

    def _build(self):
        function_type = llvmir.FunctionType(llvmir.IntType(32), [])
        function = llvmir.Function(self.module, function_type, name="main")
        block_main = function.append_basic_block("entry")
        irbuilder = llvmir.IRBuilder(block_main)
        irbuilder.position_at_end(block_main)

        for entry in self.script:
            if entry:
                entry.IR(irbuilder)

        irbuilder.ret(llvmir.Constant(llvmir.IntType(32), 0))

        # LLVM-IR ==> in-memory representation
        self.__llvm_module = llvm.parse_assembly(str(self.module))
        self.__llvm_module.verify()

    def emit(self, args):
        ret = str(self.__llvm_module)

        if args.ir:
            ending = "ll"

        if args.asm:
            ending = "S"

        if args.obj:
            ending = "obj"

        if args.dst == None:
            filename = PosixPath(args.src)
            filename = f"{filename.parent.joinpath(filename.stem)}.{ending}"
        else:
            filename = PosixPath(args.dst)

            if not filename.parent.exists():
                filename.parent.mkdir(parents=True, exist_ok=True)

        if not args.ir:
            # tm = llvm.Target.from_default_triple().create_target_machine()
            tm = llvm.Target.from_triple(self.rtl_target).create_target_machine()

            # Compile the module to machine code using MCJIT
            with llvm.create_mcjit_compiler(self.__llvm_module, tm) as ee:
                ee.finalize_object()

                if args.asm:
                    ret = tm.emit_assembly(self.__llvm_module)

                if args.obj:
                    with open(filename, "wb") as fh:
                        fh.write(tm.emit_object(self.__llvm_module))

                    ret = filename

        if not args.obj and args.dst is not None:
            with open(filename, "w") as fh:
                fh.write(str(ret))

            ret = filename

        return ret
