import math
import copy
import traceback
from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring
from lib.validators.generic import isint
from lib.core.utility import TaskClass


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module is used to download from the host and save it to the Specula server.
        On bigger files it chunks it and downloads parts of the file between each checkin. 
        Default chunksize is set to 256K.

        It uses Scripting.FileSystemObject
        - Getfile
        - OpenAsTextStream
        - Read
        - Close
        """
        self.entry = 'get_file'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "File on host you want to download. Ex: C:\\folder\\file.txt",
            "handler": quotedstring
        }
        self.options['chunksize'] = {
            "value": "256000",
            "required": True,
            "description": "Size of chunk to pull each callback (in bytes) more then 256K may result in long running script errors",
            "validator": isint
        }
        self.options['destination'] = {
            "value": None,
            "required": True,
            "description": "On disk location on your Specula server you would like this file to be downloaded to. Ex: /root/temp/file.txt",
            "handler": None,
            "tab_complete": self.helpers.complete_path
        }
        super().__init__(templatepath)

    def rethandler(self, agent, options, data):
        if len(data) > 0: # we opened the file and got a size
            try:
                with open(options['destination']['value'], 'w') as fp: # create / overwrite the file
                    pass
                size = int(data) # force valueerror if our size is off
                if size == 0:
                    self.helpers.speclog("{}: Requested file {} is empty".format(agent.hostname, options['file']['value']), output=True)
                    return
                DF = self.helpers.get_module('download_file', hidden=True) # module to download each chunk
                DF.options['file']['value'] = quotedstring(options['file']['value'])
                DF.options['startloc']['value'] = 0
                DF.options['chunksize']['value'] = \
                    int(options['chunksize']['value']) if int(options['chunksize']['value']) < size else size
                DF.options['destination']['value'] = options['destination']['value']
                DF.options['totalsize']['value'] = size
                if DF.options['chunksize']['value'] == DF.options['totalsize']['value']:
                    DF.options['done']['value'] = True
                task = TaskClass('download_file',
                                 self.helpers.renderModule(DF, agent),
                                 DF.entry,
                                 copy.deepcopy(DF.options),
                                 True,
                                 'Download File part 1 / {}'.format(math.ceil(size / int(options['chunksize']['value']))),
                                 printlog=False)
                agent.add_task(task)
            except Exception as msg:
                traceback.print_exc()
                self.helpers.speclog("{}: Failed to start file download : {}".format(agent.hostname, msg), output=True)
        else:
            self.helpers.speclog("{}: Was not able to start downloading {}, could be missing, or permissions error".format(agent.hostname, options['strFile']['value']),output=True)
