from lib.core.specmodule import SpecModule

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
Loads a dll from disk using LoadLibrary
        """
        self.entry = 'load_dll'
        self.depends = []
        self.options['dll'] = {
            "value": None,
            "required": True,
            "description": "dll to load",
            "handler": None
        }
        super().__init__(templatepath)

    def preprocess(self, agent):
        if agent.api_verified != True:
            raise RuntimeError("API has not been verified, please run api_verify first to check that the API is working\nIf it works it will mark the attribute api_verified to True\nTo override you would need to use dbedit to change the value to true")
