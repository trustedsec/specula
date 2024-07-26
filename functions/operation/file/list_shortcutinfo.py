from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring
class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Lists details about specified shortcut

        It uses WScript.Shell.CreateShortcut
        """
        self.entry = 'list_shortcutinfo'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "Path to shortcut file you want to list info about",
            "handler": quotedstring
        }
        super().__init__(templatepath)
