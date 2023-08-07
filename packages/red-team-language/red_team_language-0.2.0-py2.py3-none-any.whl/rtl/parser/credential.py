from types import SimpleNamespace
from rtl.parser.transform import Transform
from rtl.parser.helpers import helper_generate_id
from rtl.parser.helpers import helper_create_global_char_array
from rtl.parser.transform import Transform
import llvmlite.ir as ir
from rtl.parser.kvstore import KVStore


class Credential(KVStore):
    LINE_TRIGGER = "credential"

    def __init__(self, id, transform, options):
        super(Credential, self).__init__(id, transform, options)

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

            if line_tokens[0] == "username":
                options["username"] = "".join(line_tokens[1:])

            if line_tokens[0] == "password":
                options["password"] = "".join(line_tokens[1:])
                options["type"] = "password"

            if line_tokens[0] == "transform":
                transform = Transform.parse([id], fh)

        return cls(id, transform, options)
