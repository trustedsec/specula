from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the current installed PowerShell versions on the host using registry.

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).EnumKey
        - ConnectServer(root\cimv2).GetStringValue
        """
        self.entry = 'list_installedpowershell'
        self.depends = []
        super().__init__(templatepath)
        