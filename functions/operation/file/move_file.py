from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module will move a file. This can also be used to rename a file.
        
        It uses Scripting.FileSystemObject
        - MoveFile
        - FileExists
        """
        self.entry = 'move_file'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "Path and filename of source file. i.e. c:\\foo.txt.",
            "handler": quotedstring
        }
        self.options['destination'] = {
            "value": None,
            "required": True,
            "description": "Path and filename of destination file. i.e. c:\\bar.txt.",
            "handler": quotedstring
        }
        super().__init__(templatepath)