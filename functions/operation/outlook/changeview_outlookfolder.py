from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you to change the view for the user in Outlook.
        You can use this to for instance navigate the user to the calendar/tasks/junk etc

        folder option should be set to int value found here: 
        https://docs.microsoft.com/en-us/office/vba/api/outlook.oldefaultfolders
        That means, 
        outbox would be 4
        inbox would be 6
        sent would be 5
        tasks would be 13
        calendar would be 9
        junk would be 23

        It uses OutlookApplication
        - GetNameSpace("MAPI").GetDefaultFolder(VARIABLE)
        - ActiveExplorer.CurrentFolder
        """
        self.entry = 'changeview_outlookfolder'
        self.depends = []
        self.options['folder'] = {
            "value": None,
            "required": True,
            "description": "Folder to hide or unhide",
            "handler": makeint
        }
        super().__init__(templatepath)
