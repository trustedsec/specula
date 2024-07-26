from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Execute a command via cmd.exe and print any output to the agent log file.
        Uses the cmd /c prefix

        It uses Wscript.shell
        - Run

        It uses Scripting.FileSystemObject
        - OpenTextFile
        - FileExists
        - GetSpecialFolder
        - GetTempname
        - DeleteFile

        """
        self.entry = 'Execute_CMD'
        self.options['command'] = {
            "value": None,
            "required": True,
            "description": "Command to execute on remote target",
            "handler": quotedstring
        }
        super().__init__(templatepath)
