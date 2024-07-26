from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Lists interesting registry values that might be passwords 
        or other interesting configuration settings

        It uses WbemScripting.SWbemNamedValueSet
        - Add
        - Add.__ProviderArchitecture

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).EnumValues
        - ConnectServer(root\cimv2).GetDwordValue
        - ConnectServer(root\cimv2).GetStringValue
        - ConnectServer(root\cimv2).GetExpandedStringValue
        - ConnectServer(root\cimv2).GetBinaryValue
        - ConnectServer(root\cimv2).GetMultiStringValue
        - ConnectServer(root\cimv2).GetQWORDValue
        """
        self.entry = 'list_environmentvariables'
        self.depends = ['./helperFunctions/Getallregvalues.txt']
        super().__init__(templatepath)
        