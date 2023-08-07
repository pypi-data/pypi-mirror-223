from types import SimpleNamespace
from rtl.parser.transform import Transform
from rtl.parser.helpers import helper_generate_id
from rtl.parser.helpers import helper_create_global_char_array
from rtl.parser.transform import Transform
import llvmlite.ir as ir
from abc import abstractmethod, abstractclassmethod


class KVStore:
    LINE_TRIGGER = None
    KEYS = {}

    def __init__(self, id, transform, options):
        self.id = id
        self.transform = transform
        self.options = options

    @classmethod
    def parse(cls, tokens, fh):
        id = tokens[1]
        transform = SimpleNamespace(transforms=[])
        options = {}

        while True:
            line = fh.readline().strip()

            if line == "":
                break

            line_tokens = line.split(":")

            line_key = cls.KEYS.get(line_tokens[0], False)

            if line_key is not False and line_key != "transform":
                options[line_key] = "".join(line_tokens[1:])

            if line_key == "transform":
                transform = Transform.parse([id], fh)

        return cls(id, transform, options)

    def IR(self, builder):
        self.IR_options(builder)

    @property
    def function_name_options(self):
        return f"{self.id}_options"

    @staticmethod
    def get_function_name(_id):
        return f"{_id}_options"

    def IR_options(self, builder):
        func_ty = ir.FunctionType(ir.PointerType(ir.IntType(8)), [])  # function returns a char*
        func = ir.Function(builder.module, func_ty, name=self.function_name_options)
        local_builder = ir.IRBuilder(func.append_basic_block("entry"))

        kv_bytes = int.to_bytes(len(self.options) * 2, 2, "little", signed=False)

        for key, value in self.options.items():
            kv_bytes += int.to_bytes(len(key), 2, "little", signed=False)
            kv_bytes += bytes(key, "utf8")
            kv_bytes += int.to_bytes(len(value), 2, "little", signed=False)
            kv_bytes += bytes(value, "utf8")

        kv_bytes, binary_len = Transform.apply(
            f"{self.id}.{self.__class__.__name__.lower()}.options", self.transform.transforms, local_builder, kv_bytes
        )

        local_builder.ret(kv_bytes)

        setattr(self, self.function_name_options, func)  # TODO: better naming
