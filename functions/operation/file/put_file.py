import math
import copy
import os
import traceback
from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import makeint, quotedstring
from lib.core.utility import TaskClass
from datetime import datetime

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.entry = 'put_file'
        self.depends = []
        self.help = """
        This module will upload file from the Specula server to the agent. 
        It will convert the data to hex and divide it into chunks before appending
        to the file on the agent that you specify with the destination option. 
        It will create a series of tasks (one for each chunk of the file).
        Once the file has been uploaded it will compare the size on the server with the uploaded file to verify that they match.
        When the entire task is complete it will output it to the prompt.

        It uses Scripting.FileSystemObject
        - OpenTextFile
        - OpenTextFile().Write
        - OpenTextFile().Close
        """
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "File on Specula server we are uploading",
            "tab_complete": self.helpers.complete_path,
            "handler": None            
        }
        self.options['chunksize'] = {
            "value": 50048,
            "required": True,
            "description": "Default option seems to be working good. Size (50048 == 25KB) upload per callback",
            "handler": makeint
        }
        self.options['destination'] = {
            "value": None,
            "required": True,
            "description": "File on agent we are writing this to",
            "handler": quotedstring
        }
        self.options['data'] = {
            "value": None,
            "required": False,
            "description": "Placeholder for the hex data of the file",
            "handler": None,
            "handler": quotedstring,
            "hidden": True
        }
        super().__init__(templatepath)

    def preprocess(self, agent):
        try:
            chunksize = int(self.options['chunksize']['value'])
            with open(self.options['file']['value'], "rb") as a_file:
                hexdata = a_file.read().hex()
                size = len(hexdata)
                self.options['data']['value'] = hexdata
                if size == 0:
                    self.helpers.speclog("{}: Requested file {} is empty".format(agent.hostname, self.options['strFile']['value']), output=True)
                    return
            startposition = 0
            filepart = 1
            remainingdata = len(hexdata)
            while remainingdata > 0:
                UF = self.helpers.get_module('upload_file', hidden=True) # module to upload each chunk
                UF.options['file']['value'] = self.options['file']['value']
                UF.options['chunksize']['value'] = chunksize
                UF.options['destination']['value'] = self.options['destination']['value']
                if remainingdata < chunksize:
                    UF.options['data']['value'] = hexdata[startposition:startposition+remainingdata]
                    UF.options['chunksize']['value'] = remainingdata
                    remainingdata = remainingdata-remainingdata
                else:                        
                    UF.options['data']['value'] = hexdata[startposition:startposition+chunksize]
                    remainingdata = remainingdata-chunksize
                
                task = TaskClass('upload_file',
                    self.helpers.renderModule(UF, agent),
                    UF.entry,
                    copy.deepcopy(UF.options),
                    True,
                    'Upload File part {} / {}'.format(filepart, math.ceil(int(size) / int(chunksize))),
                    printlog=False)
                agent.add_task(task)
                startposition = startposition + chunksize
                filepart = filepart+1
        except Exception as msg:
                traceback.print_exc()
                self.helpers.speclog("{}: Failed to start file upload : {}".format(agent.hostname, msg), output=True)
    
    def rethandler(self, agent, options, data):
        if int(data) == int(os.path.getsize(options['file']['value'])):
            self.helpers.speclog("Finished uploading file to {} at {} - Sizes match: server:{} - agent:{}".format(agent.hostname,options['destination']['value'],str(os.path.getsize(options['file']['value'])),str(data)),output=True)
            with open("agent_data/" + agent.hostname + ".txt", "a+") as agent_log:  # A quick and dirty method to get data written to the agent log
                agent_log.write(datetime.now().strftime(self.helpers.timeformat) + " -- " + self.entry + "\n")
                agent_log.write("Uploaded file {} to {}".format(options['file']['value'], options['destination']['value']) + "\n\n")
        else:
            self.helpers.speclog("WARNING - Finished uploading file to {} at {} - Sizes are different: server:{} - agent:{}".format(
                agent.hostname,
                options['destination']['value'],
                int(os.path.getsize(options['file']['value'])),
                int(data)),
                output=True)
