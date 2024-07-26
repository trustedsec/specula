from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module runs the registerxll function in excel, allowing you to execute a DLL(XLL).
               
        XLL file must be on disk, does not work over http. The XLL can be named whatever as extension. (or nothing at all)
        
        For tips on how to create a XLL you can go here: 
        https://learn.microsoft.com/en-us/office/client-developer/excel/creating-xlls
        
        
        It uses the excel application
        - Registerxll
        """
        self.entry = 'execute_registerxll'
        self.depends = []
        self.options['input'] = {
            "value": None,
            "required": True,
            "description": "Path to xll file on disk",
            "handler": quotedstring
        }
        super().__init__(templatepath)
