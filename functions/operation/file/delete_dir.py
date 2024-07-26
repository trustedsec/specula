from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module will delete specified directory and all contents (all files and subfolders). 
        Specify folder path without trailing \\
        
        It uses Scripting.FileSystemObject
        - DeleteFolder
        - FolderExists
        """
        self.entry = 'delete_dir'
        self.depends = []
        self.options['directory'] = {
            "value": None,
            "required": True,
            "description": "Path to directory that should be deleted. i.e. c:\\parent\\random_secret_folder",
            "handler": quotedstring
        }
        super().__init__(templatepath)