from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the password policy from the current domain. 

        It uses WbemScripting.SWbemLocator
        - ConnectServer(\\root\\directory\\LDAP)
        - Query: SELECT DS_pwdProperties,DS_minPwdAge,DS_maxPwdAge,DS_minPwdLength,DS_lockoutThreshold,DS_lockoutDuration,DS_lockOutObservationWindow,DS_pwdHistoryLength FROM ds_domaindns
        """
        self.entry = 'list_passwordpolicy'
        self.depends = []

        super().__init__(templatepath)
