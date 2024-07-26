from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module is used to download from the specified url in the surl option and save it on the Specula agent.
        You specify where you want the file to be stored in the destpath option. 
        It also supports AlternateDataStreams, meaning you can specify destpath as c:\\temp\\file.txt:nothere

         It uses MSXML2.ServerXMLHTTP
        - open
        - send
        - status
        - ResponseBody

        It used ADODB.STREAM
        - Type
        - open
        - write
        - savetofile
        - close
        """
        self.entry = 'download_filehttp'
        self.depends = []
        self.options['url'] = {
            "value": None,
            "required": True,
            "description": "URL the agent will attempt to download this file from",
            "handler": quotedstring
        }
        self.options['destination'] = {
            "value": None,
            "required": True,
            "description": "path on disk the agent will attempt to write the downloaded file to",
            "handler": quotedstring
        }
        super().__init__(templatepath)
