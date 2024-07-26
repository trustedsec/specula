from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates all shortcuts in the MY_RECENT_DOCUMENTS / RECENT_FILES
        Resolved all shortcuts to the items and lists them out

        It uses WScript.Shell
        - CreateShortcut
        
        It uses Shell.Application
        - Namespace
        - Namespace().items
        """
        self.entry = 'list_recentfiles'
        self.depends = []
        super().__init__(templatepath)
        