from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the mapped drives on the host.

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select Name,ProviderName from Win32_MappedLogicalDisk
        """
        self.entry = 'list_mappeddrives'
        self.depends = []
        super().__init__(templatepath)