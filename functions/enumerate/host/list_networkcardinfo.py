from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates all the information from the network cards. 

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: SELECT * FROM Win32_NetworkAdapterConfiguration
        """
        self.entry = 'list_networkcardinfo'
        self.depends = []
        super().__init__(templatepath)
        