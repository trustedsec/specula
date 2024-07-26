from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module reads lists the content of the recycle bin
        for the current user. To download a file use get_file and 
        use the long path in the output from this module.

        It uses CreateObject("Shell.Application")
        """
        self.entry = 'list_recyclebin'
        self.depends = []
        super().__init__(templatepath)
