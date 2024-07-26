from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module reads the content of the hostsfile under
        C:\windows\system32\drivers\etc\hosts and outputs to the log. 
        This might reveal specific hosts or other domains etc.

        It uses Scripting.FileSystemObject
        - OpenTextFile
        - OpenTextFile().ReadFile.ReadAll
        """
        self.entry = 'list_hostsfile'
        self.depends = []
        super().__init__(templatepath)
