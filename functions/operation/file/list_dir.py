from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makebool,makeint
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        !WARNING - Recursing over to many files and folder might show NOT RESPONDING IN OUTLOOK. Make sure to not go too deep in recurselevels. 
        
        This module lists the directory you specify in the folderpath option.
        You can specify to recurse or not by setting the numbers of recurselevels, meaning it will list all directories under the specified folder.
        
        You can also specify filetype or filename to search for if you want. 
        Example <set filetype xml> and <set filename unattend> to search for <unattend.xml>

        The folderpath supports both C:\\windows\\ path or \\\\server.customer.intra\\share\\folder

        Also, remember that Outlook often runs in 32 bit so it will redirect to syswow64 if you use system32. 
        Instead use sysnative - c:\\windows\\sysnative\\GroupPolicy

        If you want to list directory structure in a directory set recurselevels to 1 or 2, nodir to False and nofiles to True.

        It uses Scripting.FileSystemObject
        - GetFolder
        - GetFolder().Files
        - GetBaseName
        - GetExtensionName
        - Path

        """
        self.entry = 'list_dir'
        self.depends = ['./helperFunctions/dir_lister.txt']
        self.options['directory'] = {
            "value": None,
            "required": True,
            "description": "Directory to list - Does not matter if you include a \ in the end or not",
            "handler": quotedstring
        }
        self.options['recurselevels'] = {
            "value": "0",
            "required": True,
            "description": "Number of folder levels to recurse (0 = folderpath\, 1 = folderpath\sub , 2 = folderpath\sub\sub and so on) - Default is root of the folder you specify (0)",
            "handler": makeint,
        }
        self.options['depth'] = {
            "value": "0",
            "required": True,
            "hidden": True,
            "description": "Not any reason to change this - only used for output purpose and place holder for variable",
            "handler": makeint
        }
        self.options['filetype'] = {
            "value": "*",
            "required": True,
            "description": "File type you want to list out - ex: exe or xml. To list out all, set it to * (default)",
            "handler": quotedstring
        }
        self.options['filename'] = {
            "value": "*",
            "required": True,
            "description": "File name you want to list out - ex: notepad or secret. To list out all, set it to * (default)",
            "handler": quotedstring
        }
        self.options['nodirectories'] = {
            "value": "False",
            "required": True,
            "description": "Set to True if you not want directories in the output",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}  
        }
        self.options['nofiles'] = {
            "value": "False",
            "required": True,
            "description": "Set to True if you not want files in the output",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}  
        }
        self.options['sizeformat'] = {
            "value": "mb",
            "required": True,
            "description": "Size format of files in output",
            "handler": quotedstring,
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["kb", "mb", "gb", "tb"]}  
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

        
            