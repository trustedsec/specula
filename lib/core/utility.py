import re
from lib.core.setup import gconfig
from datetime import datetime

def encrypt_code(code, key):
    Position = -1
    z = ""
    for i in range(len(code)):
        Position = Position + 1
        if Position >= len(key):
            Position = 0

        keynumber = ord(key[Position:Position + 1])
        org = ord(code[i:i + 1])
        cpt = org ^ keynumber
        cptstr = hex(cpt)[2:]
        if len(cptstr) < 2:
            cptstr = "0" + cptstr
        z = z + cptstr
    return z


def decrypt_code(code, key):
    Position = -1
    z = ""
    chars = re.findall('..', code)  # get each byte/char

    for i in range(len(chars)):
        Position = Position + 1
        if Position >= len(key):
            Position = 0

        keynumber = ord(key[Position:Position + 1])
        decstr = int(chars[i], 16) ^ keynumber  # ^ is XOR int,16 converts hex to decimal value
        z = z + chr(decstr)
    return z


class TaskClass:
    def __init__(self, funcname, code, entry, options, encrypt=True, status=None, printlog=True):
        self.name = funcname
        self.code = code
        if gconfig.DEBUG:
            print(code)
        if status is not None:
            self.status = status
        self.printlog = printlog
        self.entry = entry
        self.encrypt = encrypt
        self.options = options
        self.added = datetime.now().strftime(gconfig.TIME_FORMAT)

