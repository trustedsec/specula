from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates information about the domain the computer is joined to using WMI.
        Returns unknown if computer is in workgroup.

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select * from Win32_NTDomain
        """
        self.entry = 'list_ntdomaininfo'
        self.depends = []
        super().__init__(templatepath)
