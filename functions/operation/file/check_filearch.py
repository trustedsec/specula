from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module checks if specified file in the file option exists or not. 
        
        It uses ADODB.Stream
        - Open
        - LoadFromFile
        - Position
        - Read
        - Close
        """
        self.entry = 'check_filearch'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "path to file you want to check exists",
            "handler": quotedstring
        }
        super().__init__(templatepath)
        