#executable -> true false required to be in base, throw error if its not if true user can select this for use
#category -> string defaults to unknown
#subcategory -> string defaults to "default"
#name -> string, required
class SpecModule:
    def __init__(self, templatepath=None):
        self.templatepath = templatepath
        if not hasattr(self, 'depends'):
            self.depends = []
        if not hasattr(self, 'options'):
            self.options = {}
        if not hasattr(self, 'help'):
            self.help = "This module does not define help"
        if not hasattr(self, 'entry'):
            raise RuntimeError('Module {} does not declare a runtime entry function'.format(self))

    def set_option(self, optionname, value):
        if self._validate_option(optionname, value):
            self.options[optionname]['value'] = value
            return True
        else:
            print('Option Failed validation, refusing to set')
            return False

    def get_option(self, optionname):
        if 'handler' in self.options[optionname] and self.options[optionname]['handler'] is not None:
            args = self.options[optionname]['handlerargs'] if 'handlerargs' in self.options[optionname] else {}
            return self.options[optionname]['handler'](self.options[optionname]['value'], **args)
        return self.options[optionname]['value']

    def _validate_option(self, optionname, value):
        if 'validator' in self.options[optionname] and self.options[optionname]['validator'] is not None:
            args = self.options[optionname]['validatorargs'] if 'validatorargs' in self.options[optionname] else {}
            status = self.options[optionname]['validator'](value, **args)
            return status
        else:
            return True

    def check_required(self):
        status = True
        for k, v in self.options.items():
            if v['required'] is True and v['value'] is None:
                print(" *** Option '{}' is required but is NOT set".format(k))
                status = False
        if not status:
            raise RuntimeError("Not all required options set")
        return status

    def preprocess(self, agent):
        return

    # this isn't doing what it sounds like, so stripping it for now
    # def postprocess(self, agent):
    #     return

    #when this is call is won't be your actual module
    #this is because we are just pickling the tasks to / from disk, so that's why we are passing what seems like excessive options
    #outside of helpers, do not attempt to reference class variables in rethandler

    def rethandler(self, agent, options, data):
        return

    def cleanup(self):
        return

