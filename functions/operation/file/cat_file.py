from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module gets the content of the file specified in file
        and outputs it to the log file.
        
        It uses Scripting.FileSystemObject
        - OpenTextFile
        - FileExists
        """
        self.entry = 'cat_file'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "Path to file you want to cat",
            "handler": quotedstring
        }
        self.options['output_console'] = {
            "value": "False",
            "required": True,
            "description": "If True, it will show the output in the console",
            "hidden": True,
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}  
        }
        super().__init__(templatepath)

    def rethandler(self, agent, options, data):
        if options['output_console']['value'] == "True":
            print("\n")
            print(data)