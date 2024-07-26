from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates last boot time using WMI. 
        It queries LastBootUpTime from Win32_OperatingSystem and converts it to a readable format.

        It uses WbemScripting.SWbemLocator
        - Query: Select LastBootUpTime from Win32_OperatingSystem
        """
        self.entry = 'list_boottime'
        self.depends = []
        super().__init__(templatepath)
