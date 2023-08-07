import llvmlite.ir as ir
import llvmlite.binding as llvm

from rtl.lib.protocol.common import COMMON_LLVM_O
from rtl.lib.protocol.shell import SHELL_LLVM_O, RTL_PROTOCOL_SHELL_EXECUTION_METHODS  # recompile things...every import...so dirty...
from rtl.parser.executable import Executable
from rtl.parser.helpers import helper_generate_id

llvm.ObjectFileRef.from_path(COMMON_LLVM_O)
llvm.ObjectFileRef.from_path(SHELL_LLVM_O)

EXTERNAL_FUNCTION_TYPE = ir.FunctionType(
    ir.IntType(32),
    [
        ir.IntType(32),
        ir.PointerType(ir.IntType(8)),
        ir.IntType(32),
        ir.PointerType(ir.IntType(8)),
        ir.PointerType(ir.IntType(8)),
    ],
)


class Shell:
    EXTERNAL_FUNCTION_NAME = "protocol_shell"

    def __init__(self, options, flow, id, execution_target=[]):
        self.options = options
        self.flow = flow
        self.id = id
        self.execution_target = execution_target

    @classmethod
    def parse(cls, tokens, fh):
        options = {}
        flow = []
        id = helper_generate_id()
        execution_target = []
        icn = 0

        for entry in tokens:
            if ":" in entry:
                kva = entry.split(":").strip()
                options[kva[0]] = kva[1]

        while True:
            line = fh.readline().strip()

            if line == "" or line == "!!!":
                break

            line_tokens = line.split(" ")

            if line_tokens[0] == "expect":
                pass

            if line_tokens[0] == "send":
                pass

            if line_tokens[0] == "execute":

                if line_tokens[1] == "inline":

                    if len(line_tokens) >= 2:

                        if line_tokens[2] == "executable":
                            scriptname = f"{id}_inline_executable_{icn}"
                            execution_target.append((scriptname, Executable.parse(["", scriptname] + line_tokens[3:], fh)))
                            icn += 1

                else:
                    target = Executable.get(line_tokens[1])

                    if target is None:
                        raise Exception(f"Unknown execution target for script: {line}")

                    execution_target.append((line_tokens[1], target))

        return cls(options, flow, id, execution_target)

    @property
    def func_name(self):
        return f"{self.id}_shell"

    def IR(self, builder):
        """
        execute any and all execution_target - one at a time - in the order they were defined...
        """

        # add the extern to builder if it's not present
        try:
            protocol_shell_func = builder.module.get_global(self.EXTERNAL_FUNCTION_NAME)
        except KeyError:
            protocol_shell_func = ir.Function(builder.module, EXTERNAL_FUNCTION_TYPE, name=self.EXTERNAL_FUNCTION_NAME)

        cnt = 0

        for entry in self.execution_target:
            """
            For every script, create a 'wrapper' which invokes the execution_target function - invoked by 'main'
            """

            # unpack our tuple
            target_name, target = entry

            # function def. wrapper for external call
            func_ty = ir.FunctionType(ir.IntType(32), [])  # function returns a char*
            func = ir.Function(builder.module, func_ty, name=f"{self.func_name}_{cnt}")
            local_builder = ir.IRBuilder(func.append_basic_block("entry"))

            shell_method = RTL_PROTOCOL_SHELL_EXECUTION_METHODS.get("MEMFD", 0)

            if isinstance(target, Executable):
                target.IR(builder)
                target_function = getattr(target, target.function_name)
                target_size = getattr(target, target.data_size)
                shell_method = target.execution_method
                arvg = local_builder.call(getattr(target, target.function_name_argv), [])
                envp = local_builder.call(getattr(target, target.function_name_envp), [])
            else:
                raise Exception(f"Unknown script: {target_name}")

            target_buffer = local_builder.call(target_function, [])

            local_builder.ret(
                local_builder.call(
                    protocol_shell_func,
                    [
                        ir.Constant(
                            ir.IntType(32),
                            shell_method,
                        ),
                        target_buffer,
                        ir.Constant(ir.IntType(32), target_size),
                        arvg,
                        envp,
                    ],
                )
            )

            ret = builder.call(func, [])

            not_equal = builder.icmp_signed("!=", ret, ir.Constant(ir.IntType(32), 0))

            with builder.if_then(not_equal):
                builder.ret(ret)

            cnt += 1

            """
            TODO: once llvmlite binds to LLVM 14...or I understand more of what isn't working...until then, just link with the object file...

            mod = llvm.parse_assembly(SHELL_LLVM_IR)
            mod.verify()
            """
