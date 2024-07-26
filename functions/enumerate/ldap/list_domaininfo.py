from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates Top level information from the specified domain in the Domain option.

        It uses WbemScripting.SWbemLocator
        - ConnectServer(\\root\\directory\\LDAP)
        - Query: SELECT * FROM ds_domaindns
        """
        self.entry = 'list_domaininfo'
        self.depends = []

        super().__init__(templatepath)