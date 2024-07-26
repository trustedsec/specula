from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates autoruns defined on the agent

        It uses WbemScripting.SWbemNamedValueSet
        - Add
        - Add.__ProviderArchitecture

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).EnumValues
        - ConnectServer(root\cimv2).GetDwordValue
        - ConnectServer(root\cimv2).GetStringValue
        - ConnectServer(root\cimv2).GetExpandedStringValue
        - ConnectServer(root\cimv2).GetBinaryValue
        - ConnectServer(root\cimv2).GetMultiStringValue
        - ConnectServer(root\cimv2).GetQWORDValue

        It uses Scripting.FileSystemObject
        - GetFolder
        - GetFolder().Files
        - GetBaseName
        - GetExtensionName
        """
        self.entry = 'list_autoruns'
        self.depends = ['./helperFunctions/Getallregvalues.txt', './helperFunctions/Getregvalue.txt', './helperFunctions/dir_lister.txt']
        self.options['username'] = {
            "value": "Dummy",
            "required": True,
            "description": "Username, autoresolves to agents registered username",
            "handler": quotedstring,
            "hidden": False
        }
        super().__init__(templatepath)
    
    def preprocess(self, agent):
        self.options['username']['value'] = agent.username