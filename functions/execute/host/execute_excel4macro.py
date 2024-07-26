from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module spawns a new instance of excel and executes ExecuteExcel4Macro to execute provided call.
        ExecuteExcel4Macro("CALL(INPUT)")

        Example calling Windows API using INPUT: 
        - set input ""Kernel32"",""GetTickCount"",""J""
        - set input ""user32"",""SetCursorPos"",""JJJ"",1,2
        
        Info about the datatypes (J)
        B - 8-byte floating-point number (IEEE), Transferred by Value, C type double.
        C - Zero (null) terminated string (max. Length = 255 characters), Transferred by Reference, C type char *
        F - Zero (null) terminated string (max. Length = 255 characters), Transferred by Reference (modify in place), C type char *
        J - 4 bytes wide signed integer, Transferred by Value, C type long int
        P - Excel's OPER data structure, Transferred by Reference, C type OPER *
        R - Excel's XLOPER data structure, Transferred by Reference, C type XLOPER *
        
        It uses the excel application
        - ExecuteExcel4Macro
        """
        self.entry = 'execute_excel4macro'
        self.depends = []
        self.options['input'] = {
            "value": None,
            "required": True,
            "description": "What to execute, remember two double quotes around parameters, see help!",
            "handler": quotedstring
        }
        super().__init__(templatepath)
