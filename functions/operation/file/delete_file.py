from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module deletes the specified file in the file option.

        It uses Scripting.FileSystemObject
        - DeleteFile
        - FileExists
        """
        self.entry = 'delete_file'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "Path to file to delete",
            "handler": quotedstring
        }
        super().__init__(templatepath)
