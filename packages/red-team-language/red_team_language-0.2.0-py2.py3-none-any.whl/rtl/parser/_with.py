from rtl.parser.protocol.shell import Shell
from rtl.parser.protocol.ssh import SSH

class With:
    LINE_TRIGGER = "with"
    PROTOCOLS = {
        "shell": Shell.parse,
        "ssh": SSH.parse,
    }

    @classmethod
    def parse(cls, tokens, fh):

        protocol = tokens[1]
        options = tokens[1:]

        if protocol not in cls.PROTOCOLS.keys():
            return False

        return cls.PROTOCOLS[protocol](options, fh)
