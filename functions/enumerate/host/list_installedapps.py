from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the installed applications. 
        It enumerates information from the 
         HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ 
         &
         HKLM\\SOFTWARE\\wow6432node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ 
         registry keys.

        It uses WbemScripting.SWbemLocator
        - Add
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).EnumKey
        - ConnectServer(root\cimv2).GetStringValue
        """
        self.entry = 'list_installedapps'
        self.depends = []
        super().__init__(templatepath)
        