from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Using WMI it enumerates the installed hotfixes.
        The Win32_QuickFixEngineering is used (Same as the Powershell cmdlet get-hotfix)

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select * from Win32_QuickFixEngineering
        """
        self.entry = 'list_hotfixes'
        self.depends = []
        super().__init__(templatepath)
        