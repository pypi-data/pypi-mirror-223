import llvmlite.ir as ir

from itertools import cycle

from rtl.lib.transform.xor import XOR_LLVM_O  # recompile things...every import...so dirty...
from rtl.parser.helpers import helper_create_global_char_array

# unsigned char * transform_xor(unsigned char *key, unsigned char *plaintext, int keyLen, int ptLen)
EXTERNAL_FUNCTION_TYPE = ir.FunctionType(
    ir.PointerType(ir.IntType(8)),
    [
        ir.PointerType(ir.IntType(8)),
        ir.PointerType(ir.IntType(8)),
        ir.IntType(32),
        ir.IntType(32),
    ],
)

# unsigned char * transform_xor_<name>()
# NOTE: caller must free the returned `unsigned char *`
EXTERNAL_ENVIRONMENTAL_FUNCTION_TYPE = ir.FunctionType(
    ir.PointerType(ir.IntType(8)),
    [],
)

# libc `void free(void*)`
EXTERNAL_FUNCTION_FREE_TYPE = ir.FunctionType(
    ir.VoidType(),
    [ir.PointerType(ir.IntType(8))],
)


class XOR:
    """
    Apply XOR based obfuscation to a provided byte sequence
    """

    EXTERNAL_FUNCTION_NAME = "transform_xor"

    def __init__(self, id, line):
        self.id = f"{id}.xor"
        self.key = b""
        self.environmental = {}

        self._parse(line)

    def _parse(self, line):
        for entry in line.split(" "):
            entry = entry.strip().split(":")

            if len(entry) <= 1:
                continue

            key = entry[0]
            value = bytes(entry[1].strip(), "utf8")

            if key.startswith("key"):
                self.key = value

            if key.startswith("machineid"):
                self.environmental["machineid"] = value

            if key.startswith("bootid"):
                self.environmental["bootid"] = value

            if key.startswith("uid"):
                self.environmental["uid"] = int.to_bytes(int(entry[1].strip()), 4, "big", signed=True)

    @classmethod
    def xor(cls, data, key):  # TODO: flop data / key arg positions...
        return b"".join(
            [
                int.to_bytes(
                    m ^ k,
                    1,
                    "little",
                    signed=False,
                )
                for (m, k) in zip(data, cycle(key))
            ]
        )

    def apply(self, data):
        key = self.key
        for v in self.environmental.values():
            key = self.xor(key, v)

        output = self.xor(data, key)

        return len(output), output

    @property
    def function_name(self):
        return f"{self.id}.function.key"

    def IR(self, builder, last_layer_bytes, last_len):
        plaintext = builder.bitcast(last_layer_bytes, ir.PointerType(ir.IntType(8)))
        initial_key_len = len(self.key)

        # add the extern if it's missing
        try:
            transform_xor_function = builder.module.get_global(self.EXTERNAL_FUNCTION_NAME)
        except KeyError:
            transform_xor_function = ir.Function(builder.module, EXTERNAL_FUNCTION_TYPE, name=self.EXTERNAL_FUNCTION_NAME)

        try:
            get_key_function = builder.module.get_global(self.function_name)
        except KeyError:
            get_key_function = ir.Function(builder.module, EXTERNAL_ENVIRONMENTAL_FUNCTION_TYPE, name=self.function_name)

            local_builder = ir.IRBuilder(get_key_function.append_basic_block("entry"))

            transform_key = helper_create_global_char_array(local_builder.module, f"{self.id}.key", self.key)

            initial_key = local_builder.bitcast(transform_key, ir.PointerType(ir.IntType(8)))

            if len(self.environmental) <= 0:
                """
                When no environmental keying is in use, the key:<yourpassword> is returned directly
                """
                local_builder.ret(initial_key)
            else:
                """
                When using environmental keying - the final 'key' is derived from a number of elements derived from
                the execution environment - all function call's which eventually return the key which should be leveraged for de-obfuscation
                """
                try:
                    external_function_free = local_builder.module.get_global("free")
                except KeyError:
                    external_function_free = ir.Function(local_builder.module, EXTERNAL_FUNCTION_FREE_TYPE, name="free")

                for k, v in self.environmental.items():
                    env_function_name = f"transform_xor_{k}"

                    try:
                        transform_xor_key_function = local_builder.module.get_global(env_function_name)
                    except KeyError:
                        transform_xor_key_function = ir.Function(
                            local_builder.module, EXTERNAL_ENVIRONMENTAL_FUNCTION_TYPE, name=env_function_name
                        )

                    env_key = local_builder.call(transform_xor_key_function, [])

                    initial_key = local_builder.call(  # TODO: add error checking on function call ret?
                        transform_xor_function,
                        [
                            env_key,
                            initial_key,
                            ir.Constant(ir.IntType(32), len(v)),
                            ir.Constant(ir.IntType(32), initial_key_len),
                        ],
                    )

                    local_builder.call(external_function_free, [env_key])

                local_builder.ret(initial_key)

        v = builder.call(
            transform_xor_function,
            [
                builder.call(get_key_function, []),
                builder.bitcast(plaintext, ir.PointerType(ir.IntType(8))),
                ir.Constant(ir.IntType(32), initial_key_len),
                ir.Constant(ir.IntType(32), last_len),
            ],
        )

        return v, last_len
