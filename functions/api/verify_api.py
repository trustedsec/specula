from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Checks if the API is working or not. If this returns an error you should investigate the api installation.
        1. Is the dll present on system? The dll paths pushed through the install_api module can be found under info/dbdata.
        2. Is the necesarry registry keys present on the host?
        3. Consider re-running the api_install
        4. Could it be an EDR blocking you :INSERT SCREAMING GIF HERE:
        """
        self.entry = 'api_verify'
        self.depends = []
        super().__init__(templatepath)
    
    def rethandler(self, agent, options, data):
        if data == "False":
            agent.api_verified = False
        if data == "True":
            agent.api_verified = True