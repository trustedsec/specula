from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the local users on the current host

        It uses CreateObject("Wscript.Shell")
        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: "SELECT * FROM Win32_UserAccount WHERE LocalAccount = True"
        """
        self.entry = 'list_localusers'
        self.depends = []
        super().__init__(templatepath)
