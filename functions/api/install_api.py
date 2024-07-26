import copy
import os

from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makebool
from lib.core.utility import TaskClass

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Sets reg keys to install com object to interface with Windows API. 
        This module uploads the OutlookHelper DLL file automatically (Queued as tasks).
        In order to leverage the API modules you need to run the api_verify at least once so that the verification
        process runs on target and updates the specula database.
        """
        self.entry = 'install_api'
        self.depends = ['./helperFunctions/Setregvalue_hkcu.txt']
        self.options['file'] = {
            "value": "c:\\com-test\\v2\\specula_com.dll",
            "required": True,
            "description": "Where to upload and register api dll",
            "handler": quotedstring
        }
        self.options['addverifytask'] = {
            "value": "True",
            "required": True,
            "description": "Will add the verify task as the next task if this is set to true.",
            "handler": makebool
        }
        super().__init__(templatepath)

    def rethandler(self, agent, options, data):
        # Updating DB with the dll paths used and setting installed to true and verified to False
        arch = data[:2]

        localdll = None
        basefile = "SpeculaApi"
        if arch == "64":
            localdll = os.path.join(self.helpers.getpayloaddir(), "api/" + basefile + ".x64.dll")
            self.helpers.speclog("Identified 64 bit office install, uploading 64 bit dll", False)
            agent.officearch = "x64"
        elif arch == "32":
            localdll = os.path.join(self.helpers.getpayloaddir(), "api/" + basefile + ".dll")
            self.helpers.speclog("Identified 32 bit office install, uploading 32 bit dll", False)
            agent.officearch = "x86"
        else:
            self.helpers.speclog("Failed to detect office arch, api install failed", True)
            mod = self.helpers.get_module('api/remove_api')
            mod.options['deletedlls']['value'] = "False"
            task = TaskClass('api/remove_api',
                             self.helpers.renderModule(mod, agent),
                             mod.entry,
                             copy.deepcopy(mod.options),
                             True)
            agent.add_task(task)
            return

        # Add task to create the folder - Just in case
        folderpath = (options['file']['value']).rsplit('\\', 1)[0] #remove filename from path
        mod = self.helpers.get_module('operation/file/create_dir')
        mod.options['directory']['value'] = folderpath
        task = TaskClass('operation/file/create_dir',
                         self.helpers.renderModule(mod, agent),
                         mod.entry,
                         copy.deepcopy(mod.options),
                         True)
        agent.add_task(task)
        
        #queue dll upload
        mod = self.helpers.get_module('operation/file/put_file')
        mod.options['file']['value'] = localdll
        mod.options['destination']['value'] = options['file']['value']
        task = TaskClass('operation/file/put_file',
                         self.helpers.renderModule(mod, agent),
                         mod.entry,
                         copy.deepcopy(mod.options),
                         True)
        agent.add_task(task)
        agent.api_dll = options['file']['value']
        agent.api_installed = True
        if options['addverifytask']['value']:
            mod = self.helpers.get_module('api/verify_api')
            task = TaskClass('api/verify_api',
                                self.helpers.renderModule(mod, agent),
                                mod.entry,
                                {},
                                True)
            agent.add_task(task)