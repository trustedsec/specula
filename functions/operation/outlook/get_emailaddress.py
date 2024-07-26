from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Gets the current users email address based of the top level folder name in Outlook

        It uses OutlookApplication
        - GetNameSpace("MAPI").Folders(1).Folderpath
        """
        self.entry = 'get_emailaddress'
        self.depends = []
        super().__init__(templatepath)
