from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the status of AppLocker. 
        It returns one of the following statuses:
        - Not Enabled
        - Auditing
        - Enforced 

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).EnumKey
        - ConnectServer(root\cimv2).GetDwordValue
        - ConnectServer(root\cimv2).GetStringValue

        """
        self.entry = 'list_applocker'
        self.depends = []
        super().__init__(templatepath)
        