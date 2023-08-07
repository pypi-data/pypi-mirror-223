from copy import deepcopy

import llvmlite.ir as ir
from rtl.parser.helpers import helper_create_global_char_array


from rtl.parser.transform.xor import XOR


class Transform:
    def __init__(self, id, transforms=[]):
        self.id = self.get_id(id)
        self.transforms = transforms

    @classmethod
    def parse(cls, tokens, fh):
        """
        transform
            <transform> <optionkey>:<optionvalue>...<optionkey>:<optionvalue>
        """
        id = tokens[0]
        transforms = []
        cnt = 0

        while True:
            line = fh.readline()

            if line.strip() == "!!!":
                break

            if line.strip().startswith("xor "):
                transforms.append(XOR(f"{id}_{cnt}", line))
                cnt += 1

        return cls(id, transforms)

    @classmethod
    def get_id(cls, id):
        return f"{id}.transform"

    @classmethod
    def apply(cls, id, transforms, builder, data):
        data_len = len(data)

        for entry in transforms:
            entry.data_len, data = entry.apply(data)

        final_script_bytes = helper_create_global_char_array(builder.module, cls.get_id(id), data)

        for entry in transforms:
            final_script_bytes, data_len = entry.IR(builder, final_script_bytes, entry.data_len)

        return builder.bitcast(final_script_bytes, ir.PointerType(ir.IntType(8))), data_len
