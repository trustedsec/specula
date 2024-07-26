from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates all computers from Active Directory. 
        It returns the sAMAccountName

        It uses WbemScripting.SWbemLocator
        - ConnectServer(\\root\\directory\\LDAP)
        - Query: SELECT DS_sAMAccountName FROM ds_computer
        """
        self.entry = 'list_computers'
        self.depends = []
        super().__init__(templatepath)
        