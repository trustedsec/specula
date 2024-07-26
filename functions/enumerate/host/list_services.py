from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the services and status on the host. 
        It lists out:
        - Service name
        - State (Stopped|Started)
        - Name (Name of the running account for the service)
        - BinPath

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select * from Win32_Service
        """
        self.entry = 'list_services'
        self.depends = []
        super().__init__(templatepath)
        