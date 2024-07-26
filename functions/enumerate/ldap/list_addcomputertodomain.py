from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates ms-DS-MachineAccountQuota from LDAP and finds the SeMachineAccountPrivilege in the default domain controller policy 
        under the static path (GUID is always static for the default domain controller policy):
        \\\\domain.com\\Sysvol\\domain.com\\Policies\\{6AC1786C-016F-11D2-945F-00C04FB984F9}\\MACHINE\\Microsoft\\Windows NT\\SecEdit\\GptTmpl.inf
        
        It uses WbemScripting.SWbemLocator
        - ConnectServer(\\root\\directory\\LDAP)
        - Query: SELECT DS_ms_DS_MachineAccountQuota FROM ds_domaindns

        It uses Wscript.Shell
        - ExpandEnvironmentStrings

        It uses Scripting.FileSystemObject
        - OpenTextFile
        - OpenTextFile().readline
        - FileExists
        """
        self.entry = 'list_addcomputertodomain'
        self.depends = []
        super().__init__(templatepath)