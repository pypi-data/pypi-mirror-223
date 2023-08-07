from types import SimpleNamespace
from rtl.parser.transform import Transform
from rtl.parser.helpers import helper_generate_id
from rtl.parser.helpers import helper_create_global_char_array
from rtl.parser.transform import Transform
import llvmlite.ir as ir
from rtl.parser.kvstore import KVStore


class Host(KVStore):
    LINE_TRIGGER = "host"
    KEYS = {"transform": "transform", "ip": "ip", "port": "port"}

    def __init__(self, id, transform, options):
        super(Host, self).__init__(id, transform, options)
