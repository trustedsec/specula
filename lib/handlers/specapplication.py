#we are not able to directly initialize RequestHandler objects for single time initilization actions
#This RequestHandler objects can access anything in the application class via self.application
#Therefore we do shared single initilization here
#validated from top level
import tornado.web

class speculaApplication(tornado.web.Application):
    def __init__(self, helpers, handlers = None, default_host = None, transforms = None, **settings):
        self.helpers = helpers
        super().__init__(handlers, default_host, transforms, **settings)
