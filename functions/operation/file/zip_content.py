from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module will zip file or folder with contents specified.

        You specify the file/folder you want to zip using the path option - Full path. 
        You specify the out zip file with the zipfile option - Full path
        
        It uses Scripting.FileSystemObject
        - FileExists
        - FolderExists
        - GetBaseName
        - GetFile
        - GetFolder
        - GetFileName
        - GetParentFolderName
        - BuildPath
        - OpenTextFile
        - GetAbsolutePathName

        It uses shell.application
        - Namespace
        - Namespace().CopyHere
        """
        self.entry = 'zip_content'
        self.depends = []
        self.options['path'] = {
            "value": None,
            "required": True,
            "description": "Target path of file/folder to zip - Ex: c:\\temp\\folderwithfiles or c:\\temp\\file.exe",
            "handler": quotedstring
        }
        self.options['zipfile'] = {
            "value": None,
            "required": True,
            "description": "Path to outputted zipped file - Ex: c:\\temp\\outfile.zip",
            "handler": quotedstring
        }
        super().__init__(templatepath)
