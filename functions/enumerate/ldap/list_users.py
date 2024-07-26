from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates all users from Active Directory. 
        It returns the sAMAccountName

        It uses WbemScripting.SWbemLocator
        - ConnectServer(\\root\\directory\\LDAP)
        - Query: SELECT DS_sAMAccountName FROM ds_user
        """
        self.entry = 'list_users'
        self.depends = []
        super().__init__(templatepath)