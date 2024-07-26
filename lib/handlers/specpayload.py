import tornado
from urllib.parse import urlparse
from lib.core.setup import gconfig

class PayloadHandler(tornado.web.StaticFileHandler):
    def set_default_headers(self):
       self.set_header('Server', gconfig.SERVER_HEADER)

    #def write_error(self, status_code, **kwargs):
    #    if status_code == 404:
    #        self.redirect('http://example.com') # Fetching a default resource
