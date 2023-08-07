from types import SimpleNamespace

import llvmlite.binding as llvm
import llvmlite.ir as ir

from rtl.lib.protocol.common import COMMON_LLVM_O
from rtl.lib.protocol.ssh import SSH_LLVM_O  # recompile things...every import...so dirty...
from rtl.parser.credential import Credential
from rtl.parser.executable import Executable
from rtl.parser.helpers import helper_create_global_int, helper_generate_id, helper_parse_options
from rtl.parser.host import Host

llvm.ObjectFileRef.from_path(COMMON_LLVM_O)
llvm.ObjectFileRef.from_path(SSH_LLVM_O)

EXTERNAL_FUNCTION_TYPE_OPEN = ir.FunctionType(
    ir.PointerType(ir.IntType(32)),
    [
        ir.PointerType(ir.IntType(8)),
        ir.PointerType(ir.IntType(8)),
    ],
)

EXTERNAL_FUNCTION_TYPE_EXECUTE = ir.FunctionType(
    ir.IntType(32),
    [
        ir.PointerType(ir.IntType(32)),
        ir.PointerType(ir.IntType(8)),
        ir.PointerType(ir.IntType(8)),
    ],
)

EXTERNAL_FUNCTION_TYPE_CLOSE = ir.FunctionType(
    ir.VoidType(),
    [
        ir.PointerType(ir.IntType(32)),
    ],
)


class SSH:
    EXTERNAL_FUNCTION_NAME_OPEN = "protocol_ssh"
    EXTERNAL_FUNCTION_NAME_EXECUTE = "execute_remote"
    EXTERNAL_FUNCTION_NAME_CLOSE = "disconnect_remote"

    def __init__(self, options, flow, id, remotes=[]):
        self.options = options
        self.flow = flow
        self.id = id
        self.remotes = remotes

    @classmethod
    def parse(cls, tokens, fh):
        options = helper_parse_options(tokens)
        flow = []
        id = helper_generate_id()
        execution_target = []
        remotes = []

        while True:
            line = fh.readline().strip()

            if line == "" or line == "!!!":
                break

            line_tokens = line.split(" ")

            if line_tokens[0] == "connect":
                remote = SimpleNamespace(options=helper_parse_options(line_tokens[1:]), execution_target=[])

                while True:
                    line = fh.readline().strip()

                    if line == "" or line == "!!!":
                        break

                    line_tokens = line.split(" ")

                    if line_tokens[0] == "execute":
                        target = Executable.get(line_tokens[1])

                        if target is None:
                            raise Exception(f"Unknown execution target for script: {line}")

                        # TODO: when not a script, we have to make sure to move binary to remote first...
                        remote.execution_target.append((line_tokens[1], target))

                remotes.append(remote)

        return cls(options, flow, id, remotes)

    @property
    def function_name(self):
        return f"{self.id}_ssh"

    def IR(self, builder):
        """
        execute any and all execution_target - one at a time - in the order they were defined...
        """

        helper_create_global_int(builder.module, f"{self.id}_NULL", 0)

        try:
            builder.module.get_global(self.function_name)
            return
        except KeyError:
            # If we've not created this 'global' for this builder, then do so
            pass

        # add the extern to builder if it's not present
        try:
            protocol_ssh_func = builder.module.get_global(self.EXTERNAL_FUNCTION_NAME_OPEN)
        except KeyError:
            protocol_ssh_func = ir.Function(builder.module, EXTERNAL_FUNCTION_TYPE_OPEN, name=self.EXTERNAL_FUNCTION_NAME_OPEN)

        # add the extern to builder if it's not present
        try:
            protocol_ssh_func_execute = builder.module.get_global(self.EXTERNAL_FUNCTION_NAME_EXECUTE)
        except KeyError:
            protocol_ssh_func_execute = ir.Function(
                builder.module, EXTERNAL_FUNCTION_TYPE_EXECUTE, name=self.EXTERNAL_FUNCTION_NAME_EXECUTE
            )

        # add the extern to builder if it's not present
        try:
            protocol_ssh_func_close = builder.module.get_global(EXTERNAL_FUNCTION_TYPE_CLOSE)
        except KeyError:
            protocol_ssh_func_close = ir.Function(
                builder.module, EXTERNAL_FUNCTION_TYPE_CLOSE, name=self.EXTERNAL_FUNCTION_NAME_CLOSE
            )

        func_ty = ir.FunctionType(ir.IntType(32), [])
        func = ir.Function(builder.module, func_ty, name=f"{self.id}.ssh")
        local_builder = ir.IRBuilder(func.append_basic_block("entry"))

        for remote in self.remotes:
            credential_func = builder.module.get_global(Credential.get_function_name(remote.options.get("credential")))
            host_func = builder.module.get_global(Host.get_function_name(remote.options.get("host")))

            credential_buffer = local_builder.call(credential_func, [])
            host_buffer = local_builder.call(host_func, [])

            connection = local_builder.call(
                protocol_ssh_func,
                [
                    credential_buffer,
                    host_buffer,
                ],
            )

            not_equal = local_builder.icmp_signed(
                "!=", local_builder.ptrtoint(connection, ir.IntType(32)), ir.Constant(ir.IntType(32), 0)
            )

            with local_builder.if_else(not_equal) as (then, otherwise):
                with then:
                    for _, target in remote.execution_target:
                        if isinstance(target, Executable):
                            target.IR(local_builder)
                            target_function = getattr(target, target.function_name)
                        else:
                            raise Exception(f"Unknown script: {target}")

                        target_buffer = local_builder.call(target_function, [])
                        envp = local_builder.call(getattr(target, target.function_name_envp), [])

                        ret = local_builder.call(
                            protocol_ssh_func_execute,
                            [
                                connection,
                                target_buffer,
                                envp,
                            ],
                        )

                        not_equal = local_builder.icmp_signed("!=", ret, ir.Constant(ir.IntType(32), 0))

                        with local_builder.if_then(not_equal):
                            local_builder.ret(ret)

                    local_builder.call(
                        protocol_ssh_func_close,
                        [
                            connection,
                        ],
                    )

                    local_builder.ret(ret)

                with otherwise:
                    local_builder.ret(ir.Constant(ir.IntType(32), -1))

            local_builder.ret(ir.Constant(ir.IntType(32), -2))

            ret = builder.call(func, [])

            not_equal = builder.icmp_signed("!=", ret, ir.Constant(ir.IntType(32), 0))

            with builder.if_then(not_equal):
                builder.ret(ret)
