from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint
from lib.validators.generic import isint

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module will split the file into smaller pieces.
        Join the files back togheter with the command: copy /b c:\\temp\\filesbasename* exfile.zip

        You specify the file you want to split using the file option. 
        You specify the size per file you want in the splitsize option.
        You specify the directory you want the splitted files to be stored using the directory option.
        You specify the basename to use for the splitted files with the basename_split_files option.
        
        It uses Scripting.FileSystemObject
        - GetFile
        - FileExists
        - FolderExists
        - GetAbsolutePathName
        - BuildPath
        - CreateFolder
        - CreateTextFile

        """
        self.entry = 'split_file'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "Target path of file to split and exfiltrate",
            "handler": quotedstring
        }
        self.options['splitsize'] = {
            "value": "8",
            "required": True,
            "description": "Size in MB you want file to split into - default is 8MB",
            "handler": quotedstring,
            "validator": isint
        }
        self.options['directory'] = {
            "value": None,
            "required": True,
            "description": "Directory for splitted files, directory will get created if does not exist - Ex: c:\\temp\\outfolder",
            "handler": quotedstring
        }
        self.options['basename_split_files'] = {
            "value": None,
            "required": True,
            "description": "Basename to use for the splitted files",
            "handler": quotedstring,
        }
        super().__init__(templatepath)
