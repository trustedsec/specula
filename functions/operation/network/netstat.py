from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = r"""
        This module attempts to recreate netstat in vbscript.
        This will use the WMI class MSFT_NetTCPConnection to retrieve the info.

        It uses: 
        WbemScripting.SWbemLocator
        ConnectServer(".", "root\StandardCimv2")
        SELECT FROM MSFT_NetTCPConnection
        """
        self.entry = 'netstat'
        self.depends = []
        self.options = {}
        super().__init__(templatepath)
