from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Spawns/Executes the specified process/command under explorer.exe.
        Example: 
          set command c:\\tools\\autoruns.exe
          set arguments -e
          run
        
        It uses Shell.Application
        - Windows.app.item()
        - Windows.app.item().Document.Application.ShellExecute
        """
        self.entry = 'Spawn_Explorer'
        self.depends = []
        self.options['command'] = {
            "value": None,
            "required": True,
            "description": "Command to execute on remote target",
            "handler": quotedstring
        }
        self.options['arguments'] = {
            "value": "\"\"",
            "required": True,
            "description": "Arguments to pass to command. Default is no arguments",
            "handler": quotedstring
        }
        super().__init__(templatepath)
