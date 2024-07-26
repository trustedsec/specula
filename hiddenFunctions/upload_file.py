from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import makeint, quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.entry = 'upload_file'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "file we are uploading",
            "tab_complete": self.helpers.complete_path,
            "handler": None            
        }
        self.options['chunksize'] = {
            "value": None,
            "required": True,
            "description": "size in bytes we are uploading per callback",
            "handler": makeint
        }
        self.options['destination'] = {
            "value": None,
            "required": True,
            "description": "where we are writing this out to",
            "handler": quotedstring
        }
        self.options['data'] = {
            "value": None,
            "required": False,
            "description": "where we are writing this out to",
            "handler": None,
            "handler": quotedstring,
            "hidden": True
        }
        super().__init__(templatepath)

    def rethandler(self, agent, options, data):
        if str(data).startswith("ERROR"):
            self.helpers.speclog("Upload failed - Clear task queue manually or it will loop forever",output=True)
            self.helpers.speclog(str(data),output=True)
            
