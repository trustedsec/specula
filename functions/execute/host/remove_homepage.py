from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Removes the homepage implant in a nice way :-). 
        This should be used when you want to remove the homepage backdoor on a host.
        It removes the URL registry key as well as the EnableRoamingFolderHomepages.

        It uses WbemScripting.SWbemNamedValueSet
        - Add.__ProviderArchitecture
        - Add.__RequiredArchitecture

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).GetStringValue
        - ConnectServer(root\cimv2).DeleteValue
        """
        self.entry = 'remove_homepage'
        self.depends = []
        super().__init__(templatepath)
