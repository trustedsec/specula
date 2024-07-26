from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates all users from Active Directory that has the --Does not require password-- set. 
        It returns the sAMAccountName, ADSIPath and the useraccountcontrol value

        It uses WbemScripting.SWbemLocator
        - ConnectServer(\\root\\directory\\LDAP)
        - Query: SELECT DS_userAccountControl,DS_samaccountname FROM ds_user Where DS_userAccountControl >= 32
        """
        self.entry = 'list_passwordnotrequired'
        self.depends = []
        super().__init__(templatepath)