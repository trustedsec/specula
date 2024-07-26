from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Lists out current notification settings.
        If you get all failed in the agent log it means that it is set to default (Notifications,sounds and toasts are on)

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
        self.entry = 'list_notifications'
        self.depends = ['./helperFunctions/Getregvalue.txt']
        
        super().__init__(templatepath)