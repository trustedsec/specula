from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint
from lib.tab_completers.generic import tab_choice
from lib.validators.generic import ischoice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module gets values from the registry in the hive and path specified with the options. It is not recursive.
        !!An important thing to remember is that Outlook is in most cases running as a 32 bit application, meaning that
        when you query HKLM\Software you are basically querying HKLM\Software\Wow6432Node since that is how the 
        32 64 bit redirection works!! Specify Arch 64 to avoid the redirection

        It uses WbemScripting.SWbemNamedValueSet
        - Add.__ProviderArchitecture

        It uses WbemScripting.SWbemLocator
        ConnectServer(root\cimv2)
        ConnectServer(root\cimv2).EnumValues
        ConnectServer(root\cimv2).GetStringValue
        ConnectServer(root\cimv2).GetExpandedStringValue
        ConnectServer(root\cimv2).GetBinaryValue
        ConnectServer(root\cimv2).GetDWORDValue
        ConnectServer(root\cimv2).GetMultiStringValue
        ConnectServer(root\cimv2).GetQWORDValue
        """
        self.entry = 'GetAllValuesRegistry'
        self.depends = ['./helperFunctions/Getallregvalues.txt']
        self.options['Root'] = {
            "value": None,
            "required": True,
            "description": "Root registry to query (HKCU, HKLM, HKCR, HKU, HKCC)",
            "handler": quotedstring,
            "validator": ischoice,
            "validatorargs": {'choices': ["HKCU", "HKLM", "HKCR", "HKU", "HKCC"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["HKCU", "HKLM", "HKCR", "HKU", "HKCC"]}
        }
        self.options['PathToKey'] = {
            "value": None,
            "required": True,
            "description": "Path to the key - Example: Software\\Microsoft\\Active Setup",
            "handler": quotedstring
        }
        self.options['Arch'] = {
            "value": 64,
            "required": True,
            "description": "Architecture to query. Outlook is often 32 bit process and gets redirected to WOW6432Node, change to 64 to alter behaviour",
            "handler": makeint,
            "validator": ischoice,
            "validatorargs": {'choices': ["32", "64"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["32", "64"]}
        }
        self.options['RootInteger'] = {
            "value": None,
            "required": False,
            "description": "Root registry in INT format",
            "handler": makeint,
            "hidden": True
        }
        self.options['WMIOperation'] = {
            "value": "STDREGPROV",
            "required": True,
            "description": "Type of WMI Query method (STDREGPROV)",
            "handler": quotedstring,
            "validator": ischoice,
            "validatorargs": {'choices': ["STDREGPROV"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["STDREGPROV"]}
        }
        super().__init__(templatepath)

    def preprocess(self, agent):
        #Convert input to correct Integer needed for vbscript
        # https://docs.microsoft.com/en-us/previous-versions/windows/desktop/regprov/enumvalues-method-in-class-stdregprov
        if self.options['Root']['value'] == "HKCR":
            if self.options['WMIOperation']['value'] == "STDREGPROV":
                self.options['RootInteger']['value'] = "2147483648"
        if self.options['Root']['value'] == "HKCU":
            if self.options['WMIOperation']['value'] == "STDREGPROV":
                self.options['RootInteger']['value'] = "2147483649"
        if self.options['Root']['value'] == "HKLM":
            if self.options['WMIOperation']['value'] == "STDREGPROV":
                self.options['RootInteger']['value'] = "2147483650"            
        if self.options['Root']['value'] == "HKU":
            if self.options['WMIOperation']['value'] == "STDREGPROV":
                self.options['RootInteger']['value'] = "2147483651"          
        if self.options['Root']['value'] == "HKCC":
            if self.options['WMIOperation']['value'] == "STDREGPROV":
                self.options['RootInteger']['value'] = "2147483653"      