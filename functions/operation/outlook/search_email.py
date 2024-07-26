from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you to search mail items. Adding multiple search options adds them in a AND clause. 
        Example: Option hasattachment set to True and Subject set to %yes% becomes
        @SQL=""urn:schemas:httpmail:hasattachment""=1 AND ""urn:schemas:httpmail:subject"" like %yes%

        The gist is to use %% in the different search options unless option is provided by Specula.
        Example Search for all emails containing the word password in the subject field would be:
        set subject %password%

        Module also supports export of attachments to disk. 
        To do that set the save_attachments to True and set the export_path to the desired path on the host.
        The function will recursivly create the folders you specify. 

        If search options are missing, please create a new issue on Offpipe so it can get added.
        
        The search does not care about upper or lower case.
        
        It uses OutlookApplication
        - Session.Folders(1).folders.item(FoldersArray(0))
        - Session.Folders(1).folders.item(FoldersArray(0)).items
        """
        self.entry = 'search_email'
        self.depends = ['./helperFunctions/dir_creator.txt']
        self.options['items_to_read'] = {
            "value": 10,
            "required": True,
            "description": "The number of items to read from the top (newest first)",
            "handler": makeint
        }
        self.options['include_body'] = {
            "value": "True",
            "required": True,
            "description": "List out the body of the mail",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}  
        }
        self.options['subject'] = {
            "value": "None",
            "required": True,
            "description": "Subject to search for - supports % for wildcard. Ex: %ic% will find lick and ict.",
            "handler": quotedstring,
        }
        self.options['fromemail'] = {
            "value": "None",
            "required": False,
            "description": "Mail from to search for - supports % for wildcard. Ex: %ang% will find Lang and Dang.",
            "handler": quotedstring,
        }
        self.options['body'] = {
            "value": "None",
            "required": False,
            "description": "Body words (Do not think dirty) to search for  - supports % for wildcard. Ex: %pass% will find password and passport",
            "handler": quotedstring,
        }
        self.options['importance'] = {
            "value": "None",
            "required": False,
            "description": "Importance of emails to search for. 0=Low, 1=Normal, 2=High",
            "handler": quotedstring,
            "validator": ischoice,
            "validatorargs": {'choices': ["0", "1", "2"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["0", "1", "2"]}  
        }
        self.options['hasattachment'] = {
            "value": "False",
            "required": False,
            "description": "Search for items that only has attachments",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}  
        }
        self.options['folder_to_search'] = {
            "value": "inbox",
            "required": True,
            "description": "What folder to read emails from (Folder in freetext) - ex: inbox\\subfolder",
            "handler": quotedstring,
        }
        self.options['search_string'] = {
            "value": "None",
            "required": True,
            "description": "Search string composed by preprocessing (Auto generated)",
            "handler": quotedstring,
            "hidden": True
        }
        self.options['save_attachments'] = {
            "value": "False",
            "required": False,
            "description": "Set this to True if you want to save the attachments to disk, also set the export_path.",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}  
        }
        self.options['export_path'] = {
            "value": "None",
            "required": True,
            "description": "Export path for the attachments - Ex: C:\exportpath\subfolder",
            "handler": quotedstring,
            "hidden": False
        }        
        super().__init__(templatepath)

    def preprocess(self, agent):
        if self.options['save_attachments']['value'] == "True":
            if self.options['export_path']['value'] == "None":
                raise RuntimeError("SAVE_ATTACHMENTS is set to TRUE, but EXPORT_PATH is NOT set - Set EXPORT_PATH - Jeez")
        search_start_string = "@SQL="
        hasattachment = "\"\"urn:schemas:httpmail:hasattachment\"\""
        subject = "\"\"urn:schemas:httpmail:subject\"\""
        fromemail = "\"\"urn:schemas:httpmail:fromemail\"\""
        body = "\"\"urn:schemas:httpmail:textdescription\"\""
        importance = "\"\"urn:schemas:httpmail:importance\"\""
        constructed_search = ""

        if self.options['hasattachment']['value'] == "True":
            constructed_search = hasattachment + "=1"
        
        if self.options['subject']['value'] != "None":
            if constructed_search == "":
                constructed_search = subject + " like '" + self.options['subject']['value'] + "'"
            else:
                constructed_search = constructed_search + " AND " + subject + " like '" + self.options['subject']['value'] + "'"

        if self.options['fromemail']['value'] != "None":
            if constructed_search == "":
                constructed_search = fromemail + " like '" + self.options['fromemail']['value'] + "'"
            else:
                constructed_search = constructed_search + " AND " + fromemail + " like '" + self.options['fromemail']['value'] + "'"

        if self.options['body']['value'] != "None":
            if constructed_search == "":
                constructed_search = body + " like '" + self.options['body']['value'] + "'"
            else:
                constructed_search = constructed_search + " AND " + body + " like '" + self.options['body']['value'] + "'"

        if self.options['importance']['value'] != "None":
            if constructed_search == "":
                constructed_search = importance + "=" + self.options['importance']['value']
            else:
                constructed_search = constructed_search + " AND " + importance + "=" + self.options['importance']['value']

        self.options['search_string']['value'] = search_start_string + constructed_search