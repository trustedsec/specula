from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the local administrators on the host specified with the inMachine option

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select * from Win32_ComputerSystem
        - Query: SELECT * FROM Win32_GroupUser WHERE GroupComponent=Win32_Group.Domain=VARIABLE,Name='Administrators'
        """
        self.entry = 'list_localadmins'
        self.depends = []
        self.options['host'] = {
            "value": ".",
            "required": True,
            "description": "The machine you want to list local admins from. It defaults to localhost using .",
            "handler": quotedstring
        }
        super().__init__(templatepath)
