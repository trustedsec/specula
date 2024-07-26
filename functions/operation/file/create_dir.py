from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module creates the directory structure (recursive) 
        specified in the directory option. 

        It uses Scripting.FileSystemObject
        - GetAbsolutePathName
        - BuildPath
        - FolderExists
        - CreateFolder
        """
        self.entry = 'create_dir'
        self.depends = ['./helperFunctions/dir_creator.txt']
        self.options['directory'] = {
            "value": None,
            "required": True,
            "description": "Directory to create. i.e. c:\\parent\\child",
            "handler": quotedstring
        }
        super().__init__(templatepath)
