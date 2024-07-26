from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the installed .NET versions. 
        Based on MS documentation: 
        https://docs.microsoft.com/en-us/dotnet/framework/migration-guide/how-to-determine-which-versions-are-installed

        Lists the installed versions

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
        self.entry = 'list_installeddotnet'
        self.depends = ['./helperFunctions/Getregvalue.txt']
        super().__init__(templatepath)
        