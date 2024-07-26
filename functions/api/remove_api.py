from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makebool

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Removes the registry values set by the install_outlookhelperapi.

        """
        self.entry = 'remove_api'
        self.depends = ['./helperFunctions/Delregkey_hkcu.txt', './helperFunctions/Delregvalue_hkcu.txt']
        self.options['deletedlls'] = {
            "value": "True",
            "required": True,
            "description": "Attempt to delete dll from disk, won't work if its been loaded into outlook",
            "handler": makebool
        }
        self.options['dll'] = {
            "value": "autoresolve",
            "required": True,
            "description": "Path to file on disk, let it be autoresolve to find path in specula db",
            "handler": quotedstring
        }
        super().__init__(templatepath)
    
    def preprocess(self, agent):
        if self.options['deletedlls']['value'] == "True":
            if self.options['dll']['value'] == "autoresolve":
                if agent.api_dll:
                    self.options['dll']['value'] = agent.api_dll
                else:
                    raise RuntimeError("No value found in Specula DB for api_dll - Rerun and specify path manually or set deletedlls to False")

    def rethandler(self, agent, options, data):
        # Updating DB with the dll paths used and setting installed to true and verified to False
        agent.api_dll = None
        agent.api_installed = False
        agent.api_verified = False
    