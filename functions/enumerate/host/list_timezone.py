from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring
from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Finds the name of the current timezone for the agent

        It uses WbemScripting.SWbemNamedValueSet
        - Add.__ProviderArchitecture

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).GetStringValue
        """
        self.entry = 'list_timezone'
        self.depends = []
        super().__init__(templatepath)
    
    def rethandler(self, agent, options, data):
        agent.timezone = data