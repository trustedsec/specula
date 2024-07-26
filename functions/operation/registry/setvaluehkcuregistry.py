from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring
from lib.tab_completers.generic import tab_choice
from lib.validators.generic import ischoice


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module sets values in the HKCU hive specified with the options. 

        It uses WbemScripting.SWbemNamedValueSet
        - Add.__ProviderArchitecture

        It uses WbemScripting.SWbemLocator
        ConnectServer(root\cimv2)
        ConnectServer(root\cimv2).CreateKey
        ConnectServer(root\cimv2).SetStringValue
        ConnectServer(root\cimv2).SetDWORDValue
        """
        self.entry = 'SetValue_HKCU_Registry'
        self.depends = ['./helperFunctions/Setregvalue_hkcu.txt']
        self.options['PathToKey'] = {
            "value": None,
            "required": True,
            "description": "Path to reg key",
            "handler": quotedstring
        }
        self.options['RegType'] = {
            "value": None,
            "required": True,
            "description": "Reg key type",
            "handler": quotedstring,
            "validator": ischoice,
            "validatorargs": {'choices': ["REG_SZ", "REG_DWORD"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["REG_SZ", "REG_DWORD"]},
        }
        self.options['ValueName'] = {
            "value": None,
            "required": True,
            "description": "Name of value for entry",
            "handler": quotedstring
        }
        self.options['Value'] = {
            "value": None,
            "required": True,
            "description": "Value you want to set",
            "handler": quotedstring
        }
        super().__init__(templatepath)
