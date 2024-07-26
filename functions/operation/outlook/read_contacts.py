from lib.core.specmodule import SpecModule

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you to read the contacts items. 
        Distribution groups are not implemented yet.
        
        It uses OutlookApplication
        - GetNameSpace("MAPI").GetDefaultFolder(10)
        - GetNameSpace("MAPI").GetDefaultFolder(10).items
        """
        self.entry = 'read_contacts'
        self.depends = []
        super().__init__(templatepath)