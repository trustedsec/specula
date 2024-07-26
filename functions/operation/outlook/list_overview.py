from lib.core.specmodule import SpecModule

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module lists the structure inside outlook to 3 levels deep. Showing folders and number of items inside.
        * Deleted Items - items: 45
        ** RSS - items: 0
        * Inbox - items: 10
        ** TestFolder - items: 1
        ** test2 - items: 0
        *** level3 - items: 5
        * Outbox - items: 0
        * Sent Items - items: 2
        * Archive - items: 7

        It uses OutlookApplication
        - GetNameSpace("MAPI").Folders()
        """
        self.entry = 'list_overview'
        super().__init__(templatepath)
