import shlex
from pathlib import PosixPath
import llvmlite.ir as ir

from itertools import cycle
from types import SimpleNamespace

from rtl.parser.transform import Transform
from rtl.parser.helpers import helper_generate_id


class Executable:
    LINE_TRIGGER = "executable"
    EXECUTABLES = {}
    RTL_PROTOCOL_SHELL_BINARY_EXECUTION_METHODS = {"MEMFD": 0, "TEMPFS": 1}

    def __init__(self, id, content, transform, options):
        if self.EXECUTABLES.get(id, False):
            raise Exception(f"Multiple instances of {id} found - pick a different identifier...!")

        self.id = id
        self.content = content
        self.transform = transform
        self.options = options

        self.EXECUTABLES[self.id] = self

    @classmethod
    def get(cls, name):
        return cls.EXECUTABLES.get(name, None)

    @classmethod
    def parse(cls, tokens, fh):
        """
        parse takes input in such as the following:

        *executable* :name:somethingcool :path:/the/path/to/the/binary
        *transform*
            `type`:option anotheroptionkey:anotheroptionvalue ...
            ...
        !!!

        For example, the following is a valid script:

            ```
            executable mync :path:/home/user/nc :argv: -l -k 127.0.0.1 55555 :name:/usr/sbin/cupsd
            transform
                xor:thisisthekey
            !!!

            ```
        Another example script:
            ```
            executable whoisthat :path:/tmp/test.sh :name:/usr/sbin/cupsd
            transform
                xor:thisisthekey
            !!!

            ```

        Another example script:
            ```
            executable whoisthat :path:/bin/sh :name:/usr/sbin/cupsd
            content
                echo "this is a test" > /tmp/testing_testing_1_2_3
            !!!
            transform
                xor:thisisthekey
            !!!

            ```

        Note: the empty line at the end - this is a must...
        Note: the transform 'section' ends with a triple bang i.e. !!! - this is a must...for now - forgive me Ptah...
        """
        id = tokens[1]
        options = SimpleNamespace(
            method=False,
            name=False,
            path=False,
            argv=[],
            envp=[],
        )
        content = ""
        transform = SimpleNamespace(transforms=[])

        tokens = " ".join(tokens[2:]).split(":")

        c = 0
        for token in tokens:
            if "method" == token:
                options.method = tokens[c + 1].strip()

            if "name" == token:
                options.name = tokens[c + 1].strip()

            if "path" == token:
                options.path = tokens[c + 1].strip()

            if "envp" == token:
                options.envp = shlex.split(tokens[c + 1].strip())

            if "argv" == token:
                options.argv = shlex.split(tokens[c + 1].strip())

            c += 1

        while True:
            line = fh.readline().strip()

            if line == "" or line == "!!!":
                break

            line_tokens = line.split(" ")

            if line_tokens[0] == "content":
                while True:
                    line = fh.readline()

                    if len(line.strip()) > 0 and line.strip()[0] == "#":
                        continue

                    if line.strip() == "!!!":
                        break

                    content += line

                continue

            if line_tokens[0] == "transform":
                transform = Transform.parse([id], fh)

        return cls(id, content, transform, options)

    def IR(self, builder):
        """
        Copy a 'binary' with transforms if requested
        """

        try:
            builder.module.get_global(self.function_name)
            return
        except KeyError:
            # If we've not created this 'global' for this builder, then do so
            pass

        self.IR_binary(builder)
        self.IR_argv(builder)
        self.IR_envp(builder)

    @property
    def execution_method(self):
        return self.RTL_PROTOCOL_SHELL_BINARY_EXECUTION_METHODS.get(self.options.method, 0)

    @property
    def function_name(self):
        return f"{self.id}.binary"

    @property
    def data_name(self):
        return f"{self.id}.data"

    @property
    def data_size(self):
        return f"{self.id}.data_size"

    def IR_binary(self, builder):
        filepath = str(self.options.path)

        if filepath == False and self.content == "":
            raise Exception(f"The option :path: option or content block is required - example :path:/bin/sh")

        executable_bytes = b""

        binary_path = PosixPath(filepath)

        if self.content != "":
            executable_bytes = bytes(self.content, "utf8") + b"\x00"
            shell = self.options.path

            if shell:
                if "#!" not in shell:
                    shell = f"#!{shell}"

            else:
                shell = "#!/bin/sh"

            executable_bytes = bytes(shell, "utf8") + b"\n" + executable_bytes
        else:
            if not binary_path.exists() or not binary_path.is_file():
                raise Exception(f"binary does not exist at path : {binary_path}")

            with open(binary_path, "rb") as fh:
                executable_bytes = fh.read()

        func_ty = ir.FunctionType(ir.PointerType(ir.IntType(8)), [])  # function returns a char*
        func = ir.Function(builder.module, func_ty, name=self.function_name)
        local_builder = ir.IRBuilder(func.append_basic_block("entry"))

        executable_bytes, binary_len = Transform.apply(self.id, self.transform.transforms, local_builder, executable_bytes)

        local_builder.ret(executable_bytes)

        setattr(self, self.function_name, func)  # TODO: better naming
        setattr(self, self.data_name, executable_bytes)  # TODO: better naming
        setattr(self, self.data_size, binary_len)  # TODO: better naming

    # argv/envp code is wet - don't care atm tho...

    @property
    def function_name_argv(self):
        return f"{self.id}.argv"

    @property
    def argv_data(self):
        return f"{self.id}.argv.bytes"

    @property
    def argv_size(self):
        return f"{self.id}.argv.size"

    def IR_argv(self, builder):
        name = self.options.name

        if name == False:
            name = self.id

        # argv[0] is the binary name in the process list
        self.options.argv.insert(0, name)

        func_ty = ir.FunctionType(ir.PointerType(ir.IntType(8)), [])  # function returns a char*
        func = ir.Function(builder.module, func_ty, name=self.function_name_argv)
        local_builder = ir.IRBuilder(func.append_basic_block("entry"))

        argv_bytes = int.to_bytes(len(self.options.argv), 2, "little", signed=False)

        for argv in self.options.argv:
            argv_bytes += int.to_bytes(len(argv), 2, "little", signed=False)
            argv_bytes += bytes(argv, "utf8")

        argv_bytes, binary_len = Transform.apply(f"{self.id}.argv", self.transform.transforms, local_builder, argv_bytes)

        local_builder.ret(argv_bytes)

        setattr(self, self.function_name_argv, func)  # TODO: better naming
        setattr(self, self.argv_data, argv_bytes)  # TODO: better naming
        setattr(self, self.argv_size, binary_len)  # TODO: better naming

    @property
    def function_name_envp(self):
        return f"{self.id}.envp"

    @property
    def envp_data(self):
        return f"{self.id}.envp.bytes"

    @property
    def envp_size(self):
        return f"{self.id}.envp.size"

    def IR_envp(self, builder):
        func_ty = ir.FunctionType(ir.PointerType(ir.IntType(8)), [])  # function returns a char*
        func = ir.Function(builder.module, func_ty, name=self.function_name_envp)
        local_builder = ir.IRBuilder(func.append_basic_block("entry"))

        envp_bytes = int.to_bytes(len(self.options.envp), 2, "little", signed=False)

        for envp in self.options.envp:
            envp_bytes += int.to_bytes(len(envp), 2, "little", signed=False)
            envp_bytes += bytes(envp, "utf8")

        envp_bytes, binary_len = Transform.apply(f"{self.id}.envp", self.transform.transforms, local_builder, envp_bytes)

        local_builder.ret(envp_bytes)

        setattr(self, self.function_name_envp, func)  # TODO: better naming
        setattr(self, self.envp_data, envp_bytes)  # TODO: better naming
        setattr(self, self.envp_size, binary_len)  # TODO: better naming
