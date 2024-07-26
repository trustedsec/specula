from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This might come as a big shock, but this function stops Outlook. 
        I know, it is mindblowing.

        It uses OutlookApplication
        - Quit()
        """
        self.entry = 'Stop_Outlook'
        self.depends = []
        super().__init__(templatepath)
