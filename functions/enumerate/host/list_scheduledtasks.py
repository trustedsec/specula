from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the scheduled tasks on the host. 

        It uses WbemScripting.SWbemLocator
        - ConnectServer(ROOT\Microsoft\Windows\TaskScheduler)
        - Query: SELECT * FROM MSFT_ScheduledTask
        """
        self.entry = 'list_scheduledtasks'
        self.depends = []
        super().__init__(templatepath)
        