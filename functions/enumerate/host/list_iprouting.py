from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the IP Routing table using the Win32_IP4RouteTable and the Win32_IP4PersistedRouteTable classes.
        (Only a few selected attributes is dumped)
        Official documentation: 
         - https://docs.microsoft.com/en-us/previous-versions/windows/desktop/wmiiprouteprov/win32-ip4routetable  
         - https://docs.microsoft.com/en-us/previous-versions/windows/desktop/wmiiprouteprov/win32-ip4persistedroutetable

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: SELECT * FROM Win32_IP4RouteTable
        - Query: SELECT * FROM Win32_IP4PersistedRouteTable
        """
        self.entry = 'list_iprouting'
        self.depends = []
        super().__init__(templatepath)
        