from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module will copy a directory including all subdirectories/files. 
        Specify paths without trailing \\.
        
        It uses Scripting.FileSystemObject
        - CopyFolder
        - FolderExists
        """
        self.entry = 'copy_dir'
        self.depends = []
        self.options['directory'] = {
            "value": None,
            "required": True,
            "description": "Directory you want to copy. i.e. c:\\folder",
            "handler": quotedstring
        }
        self.options['destination'] = {
            "value": None,
            "required": True,
            "description": "Destination directory you want your copy. i.e. c:\\copyoffolder",
            "handler": quotedstring
        }
        super().__init__(templatepath)