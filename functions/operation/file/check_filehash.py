from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module gets the MD5 hash of the file specified.
        
        It uses System.Security.Cryptography.MD5CryptoServiceProvider
        - ComputeHash_2
        - Hash

        It uses ADODB.Stream
        - Open
        - LoadFromFile
        - Position
        - Read
        - Close

        It uses MSXML2.DOMDocument
        - CreateElement
        """
        self.entry = 'check_filehash'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "path to file you want to get MD5 hash for",
            "handler": quotedstring
        }
        super().__init__(templatepath)
        