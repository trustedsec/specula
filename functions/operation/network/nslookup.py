from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = r"""
        This module attempts to recreate nslookup in vbscript.
        This will use the WMI class Win32_PingStatus to ping the host and get the IP address.
        Resolving the IP will fail if ping is not allowed.

        It uses: 
        WbemScripting.SWbemLocator
        ConnectServer(".", "root\cimv2")
        SELECT * FROM Win32_PingStatus WHERE Address
        """
        self.entry = 'nslookup'
        self.depends = []
        self.options['hostname'] = {
            "value": None,
            "required": True,
            "description": "Hostname to resolve",
            "handler": quotedstring
        }
        super().__init__(templatepath)
