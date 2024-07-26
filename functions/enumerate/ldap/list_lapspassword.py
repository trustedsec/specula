from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the LAPS passwords in the current domain. 

        It uses WbemScripting.SWbemLocator
        - ConnectServer(\\root\\directory\\LDAP)
        - Query: SELECT DS_ms_Mcs_AdmPwd,DS_sAMAccountName,DS_ms_Mcs_AdmPwdExpirationTime FROM ds_computer Where DS_ms_Mcs_AdmPwd != NULL
        """
        self.entry = 'list_lapspassword'
        self.depends = []

        super().__init__(templatepath)
