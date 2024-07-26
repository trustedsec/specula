from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the computer specified in the samaccountName option. 
        If computer account is found it also enumerates the properties of the account.
        If account not found it will say so in the returned data.

        Remember to specify with $ in the end. 
        Like: set samaccountname dc1$
        
        It uses WbemScripting.SWbemLocator
        - ConnectServer(\\root\\directory\\LDAP)
        - Query: SELECT * FROM ds_computer Where DS_sAMAccountName = VARIABLE
        """
        self.entry = 'list_computer'
        self.depends = []
        self.options['samaccountname'] = {
            "value": None,
            "required": True,
            "description": "samaccountname to retreive information for",
            "handler": quotedstring
        }
        super().__init__(templatepath)
