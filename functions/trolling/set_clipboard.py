from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you to specify text as input and it will add it to the clipboard

        It uses htmlfile
        - ParentWindow.ClipboardData.SetData()

        """
        self.entry = 'set_clipboard'
        self.depends = []
        
        self.options['clipboardtext'] = {
            "value": None,
            "required": True,
            "description": "Text you want to add to the clipboard",
            "handler": quotedstring
        }
        super().__init__(templatepath)
