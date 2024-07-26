from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint,escapequotes
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module creates a shortcut file at specified file path. 
        
        It uses CreateObject("WScript.Shell")
        - CreateShortcut
        """
        self.entry = 'create_shortcut'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "Shortcut to create i.e. c:\\folder\\short.lnk",
            "handler": quotedstring
        }
        self.options['targetpath'] = {
            "value": None,
            "required": True,
            "description": "What the shortcut executes i.e. c:\\folder\\program.exe",
            "handler": quotedstring
        }
        self.options['arguments'] = {
            "value": "\"\"",
            "required": False,
            "description": "Arguments to the execution i.e. /force",
            "handler": quotedstring
        }
        self.options['description'] = {
            "value": "\"\"",
            "required": False,
            "description": "Shortcut description",
            "handler": quotedstring
        }
        self.options['hotkey'] = {
            "value": "\"\"",
            "required": False,
            "description": "Hotkey assignment i.e. CTRL+ALT+Y",
            "handler": quotedstring
        }
        self.options['iconlocation'] = {
            "value": "%SystemRoot%\System32\SHELL32.dll,166",
            "required": False,
            "description": "Icon location for Shortcut i.e. c:\\folder\\file.ico",
            "handler": quotedstring
        }
        self.options['windowstyle'] = {
            "value": "minimized",
            "required": True,
            "description": "How to execute shortcut",
            "validator": ischoice,
            "validatorargs": {'choices': ['minimized', 'normal', 'maximized']},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ['minimized', 'normal', 'maximized']}
        }
        self.options['windowstyle_int'] = {
            "value": 7,
            "required": True,
            "description": "How to execute shortcut",
            "handler": makeint,
            "hidden": True
        }
        self.options['workingdirectory'] = {
            "value": "\"\"",
            "required": False,
            "description": "Shortcut working directory i.e. c:\\folder",
            "handler": quotedstring
        }
        super().__init__(templatepath)

    def preprocess(self, agent):
        if self.options['windowstyle']['value'] == "minimized":
            self.options['windowstyle_int']['value'] = 7
        if self.options['windowstyle']['value'] == "normal":
            self.options['windowstyle_int']['value'] = 1
        if self.options['windowstyle']['value'] == "maximized":
            self.options['windowstyle_int']['value'] = 3