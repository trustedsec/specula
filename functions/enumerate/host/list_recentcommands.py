from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates recent executed commands from the registry
        HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU

        It uses WbemScripting.SWbemNamedValueSet
        - Add.__ProviderArchitecture

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).EnumValues
        - ConnectServer(root\cimv2).GetStringValue
        - ConnectServer(root\cimv2).GetExpandedStringValue
        - ConnectServer(root\cimv2).GetBinaryValue
        - ConnectServer(root\cimv2).GetDWORDValue
        - ConnectServer(root\cimv2).GetMultiStringValue
        - ConnectServer(root\cimv2).GetQWORDValue
        """
        self.entry = 'list_recentcommands'
        self.depends = ['./helperFunctions/Getallregvalues.txt']
        super().__init__(templatepath)
        