from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Lists the structure and items in the start menu.

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select Name from Win32_LogicalProgramGroupItem
        """
        self.entry = 'list_startmenu'
        self.depends = []
        super().__init__(templatepath)
        