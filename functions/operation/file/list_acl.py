from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module lists the ACL for the specified file or folder in the Path option. 

        It uses WbemScripting.SWbemLocator:
        - Query: Select * from win32_logicalFileSecuritySetting WHERE Path=
        -- GetSecurityDescriptor        
        """
        self.entry = 'list_acl'
        self.depends = []
        self.options['path'] = {
            "value": None,
            "required": True,
            "description": "Path to file or folder you want to see ACL's for",
            "handler": quotedstring
        }
        super().__init__(templatepath)
        