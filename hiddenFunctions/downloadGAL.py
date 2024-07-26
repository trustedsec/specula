import math
import copy
import traceback
from lib.core.specmodule import SpecModule
from lib.core.utility import TaskClass

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.entry = 'downloadGAL'
        self.depends = []
        self.options['curloc'] = {
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
        self.options['dest'] = {
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
        if len(data) > 0:  # we opened the file and got a size
            try:
                lines = data.split('\n')
                with open(options['dest']['value'] + '.contacts', 'a') as contacts:
                    with open(options['dest']['value'] + '.ExchangeUsers', 'a') as ExchangeUsers:
                        with open(options['dest']['value'] + '.Distros', 'a') as Distros:
                            for line in lines:
                                if line[:1] == 'C':
                                    line = line[1:] + '\n'
                                    contacts.write(line)
                                elif line[:1] == 'E':
                                    line = line[1:] + '\n'
                                    ExchangeUsers.write(line)
                                elif line[:1] == 'D':
                                    line = line[1:] + '\n'
                                    Distros.write(line)
                                else:
                                    continue
                if not options['done']['value']:  # we got data and we have more to download
                    size = int(options['totalsize']['value'])
                    sizeleft = \
                        int(options['totalsize']['value']) - \
                        (int(options['curloc']['value']) + int(options['chunksize']['value']))
                    DF = self.helpers.get_module('downloadGAL', hidden=True)  # module to download each chunk
                    DF.options['curloc']['value'] = int(options['curloc']['value']) + int(
                        options['chunksize']['value'])
                    DF.options['chunksize']['value'] = \
                        int(options['chunksize']['value']) if int(options['chunksize']['value']) < sizeleft \
                            else sizeleft
                    DF.options['dest']['value'] = options['dest']['value']
                    DF.options['totalsize']['value'] = options['totalsize']['value']
                    if DF.options['chunksize']['value'] + DF.options['curloc']['value'] == DF.options['totalsize'][
                        'value']:
                        DF.options['done']['value'] = True
                        DF.options['chunksize']['value'] += 1
                    task = TaskClass('downloadGAL',
                                     self.helpers.renderModule(DF, agent),
                                     DF.entry,
                                     copy.deepcopy(DF.options),
                                     True,
                                     'Download GAL part {} / {}'.format(
                                         math.ceil(int(DF.options['curloc']['value']) / int(
                                             options['chunksize']['value'])) + 1,
                                         math.ceil(size / int(options['chunksize']['value']))
                                     ),
                                     printlog=False
                                     )
                    agent.add_task(task)
                else:  # this was our last chunk
                    self.helpers.speclog("{}: Finished downloading GAL it was written to {}".format(
                        agent.hostname,
                        options['dest']['value']),
                        output=True)
            except Exception as msg:
                traceback.print_exc()
                self.helpers.speclog("{}: Failed to continue GAL download : {}".format(agent.hostname, msg), output=True)

        else:
            self.helpers.speclog('{}: an unknown error occurred in the middle of downloading GAL, stopping'.format(
                agent.hostname, output=True))