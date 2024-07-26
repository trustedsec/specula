import math
import copy
import traceback
from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring
from lib.core.utility import TaskClass
from datetime import datetime

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.entry = 'download_file'
        self.depends = []
        self.options['file'] = {
            "value": None,
            "required": True,
            "description": "file we are downloading",
            "handler": None
        }
        self.options['startloc'] = {
            "value": None,
            "required": True,
            "description": "offset into file we need to download at",
            "handler": None
        }
        self.options['chunksize'] = {
            "value": None,
            "required": True,
            "description": "size in bytes we are downloading per callback",
            "handler": None
        }
        self.options['destination'] = {
            "value": None,
            "required": True,
            "description": "where we are writing this out to",
            "handler": None
        }
        self.options['totalsize'] = {
            "value": None,
            "required": True,
            "description": "Total size of this file",
            "handler": None
        }
        self.options['done'] = {
            "value": False,
            "required": True,
            "description": "This is set to true when sending the last download chunk",
            "handler": None
        }
        super().__init__(templatepath)

    def rethandler(self, agent, options, data):
        if len(data) > 0: # we opened the file and got a size
            try:
                with open(options['destination']['value'], 'ab') as fp:
                    fp.write(data.encode('latin1'))
                if not options['done']['value']:  # we got data and we have more to download
                    size = int(options['totalsize']['value'])
                    sizeleft = \
                        int(options['totalsize']['value']) - \
                        ( int(options['startloc']['value']) + int(options['chunksize']['value']))
                    DF = self.helpers.get_module('download_file', hidden=True)  # module to download each chunk
                    DF.options['file']['value'] = quotedstring(options['file']['value'])
                    DF.options['startloc']['value'] = int(options['startloc']['value']) + int(options['chunksize']['value'])
                    DF.options['chunksize']['value'] = \
                        int(options['chunksize']['value']) if int(options['chunksize']['value']) < sizeleft \
                        else sizeleft
                    DF.options['destination']['value'] = options['destination']['value']
                    DF.options['totalsize']['value'] = options['totalsize']['value']
                    if DF.options['chunksize']['value'] + DF.options['startloc']['value'] == DF.options['totalsize']['value']:
                        DF.options['done']['value'] = True
                    task = TaskClass('download_file',
                                     self.helpers.renderModule(DF, agent),
                                     DF.entry,
                                     copy.deepcopy(DF.options),
                                     True,
                                     'Download File part {} / {}'.format(
                                         math.ceil(int(DF.options['startloc']['value']) / int(
                                             options['chunksize']['value'])) + 1,
                                         math.ceil(size / int(options['chunksize']['value']))
                                     ),
                                     printlog=False
                                     )
                    agent.add_task(task)
                else: # this was our last chunk
                    self.helpers.speclog("{}: Finished downloading file {} it was written to {}".format(
                        agent.hostname,
                        options['file']['value'], options['destination']['value']),
                        output=True)
                    with open("agent_data/" + agent.hostname + ".txt", "a+") as agent_log:  # A quick and dirty method to get data written to the agent log
                        agent_log.write(datetime.now().strftime(self.helpers.timeformat) + " -- " + self.entry + "\n")
                        agent_log.write("Downloaded file {} to {}".format(options['file']['value'], options['destination']['value']) + "\n\n")
            except Exception as msg:
                traceback.print_exc()
                self.helpers.speclog("{}: Failed to continue file download : {}".format(agent.hostname, msg), output=True)
        else:
            self.helpers.speclog('{}: an unknown error occured in the middle of downloading {}, stopping'.format(
                agent.hostname,
                options['file']['value']),
                output=True)