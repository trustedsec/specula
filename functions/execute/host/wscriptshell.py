from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module executes command defined in the command option through the wscript com object. 
        The executed file will become a sub-process under outlook.exe. 
        Normally NOT OPSEC SAFE

        It uses Wscript.shell
        - run
        """
        self.entry = 'Execute_WscriptShell'
        self.depends = []
        self.options['command'] = {
            "value": None,
            "required": True,
            "description": "command to execute via wscript com object",
            "handler": quotedstring
        }
        super().__init__(templatepath)
