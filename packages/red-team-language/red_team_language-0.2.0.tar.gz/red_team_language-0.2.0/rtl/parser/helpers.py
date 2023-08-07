import llvmlite.ir as ir

import random
import string

GENERATE_ID_SET = string.ascii_lowercase + string.ascii_uppercase


def helper_create_global_char_array(module, symbol_name, data):
    """
    helper_create_global_variable
        module - the llvmlite module
        symbol_name - what to call the thing
        data - the value to set the thing to

    create or locate and then return the symbol defined as 'symbol_name'
    """
    try:
        gv = module.get_global(symbol_name)
    except KeyError:
        data_len = len(data)
        gv = ir.GlobalVariable(
            module,
            ir.ArrayType(ir.IntType(8), data_len),
            symbol_name,
        )
        gv.global_constant = False
        gv.linkage = "private"
        gv.align = 1
        gv.initializer = ir.Constant(
            ir.ArrayType(ir.IntType(8), data_len),
            [i for i in data],
        )

    return gv


def helper_parse_options(tokens):
    options = {}

    for entry in tokens:
        if ":" in entry and isinstance(entry, str):
            kva = entry.split(":")
            options[kva[0]] = kva[1]

    return options


def helper_create_global_int(module, symbol_name, value):
    gv = ir.GlobalVariable(
        module,
        ir.IntType(32),
        symbol_name,
    )
    gv.global_constant = False
    gv.linkage = "private"
    gv.align = 1
    gv.initializer = ir.Constant(
        ir.IntType(32),
        value,
    )

    return gv


def helper_generate_id():
    return "".join(random.sample(GENERATE_ID_SET, 8))
