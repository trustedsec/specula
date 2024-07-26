from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates status of logging on the host. 
        It figures out status on logging settings for:
        - ProcessCreationIncludeCmdLine
        - PowerShell Script Block Logging
        - PowerShell Transcript Logging

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).EnumKey
        - ConnectServer(root\cimv2).GetDWORDValue
        """
        self.entry = 'list_logging'
        self.depends = []
        super().__init__(templatepath)
        