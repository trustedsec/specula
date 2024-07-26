from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the AMSI Providers registered on the system.
        Based on MS documentation: 
        https://techcommunity.microsoft.com/t5/exchange-team-blog/more-about-amsi-integration-with-exchange-server/ba-p/2572371
        Gets the GUID and figures out the names from the Classes\\guid table in registry
        
        It uses WbemScripting.SWbemNamedValueSet
        - Add
        - Add.__ProviderArchitecture

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).EnumKey
        - ConnectServer(root\cimv2).GetStringValue
        """
        self.entry = 'list_amsiproviders'
        super().__init__(templatepath)
        