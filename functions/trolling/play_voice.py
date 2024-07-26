from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import makeint, quotedstring
from lib.tab_completers.generic import tab_choice
from lib.validators.generic import ischoice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This is a troll module, allows you to specify text as input and it will read it out loud on the speaker using sapi.spvoice 

        It uses sapi.spvoice
        - Voice
        - speak
        """
        self.entry = 'play_voice'
        self.depends = []
        
        self.options['speaktext'] = {
            "value": None,
            "required": True,
            "description": "Text you want to say on the computer",
            "handler": quotedstring
        }
        self.options['voicegender'] = {
            "value": 0,
            "required": True,
            "description": "0 == male, and 1 == female",
            "handler": makeint,
            "validator": ischoice,
            "validatorargs": {'choices': ["0", "1"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["0", "1"]}
        }
        super().__init__(templatepath)
