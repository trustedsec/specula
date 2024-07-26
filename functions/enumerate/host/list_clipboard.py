from lib.core.specmodule import SpecModule
from datetime import datetime

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Creates a html object and retrieved the content from the clipboard

        It uses htmlfile
        - ParentWindow.ClipboardData.GetData()
        """
        self.entry = 'list_clipboard'
        self.depends = []
        super().__init__(templatepath)
