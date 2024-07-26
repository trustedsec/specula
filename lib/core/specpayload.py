import secrets
import os
import base64
import random
import shutil
import string
from collections import UserList
from datetime import datetime
from lib.core.setup import gconfig

class PayloadListClass(UserList):
    def __init__(self):
        super().__init__()

    def get_payload_id(self, id):
        for payload in self:
            if payload.id == id:
                return payload
        return None

    def get_payload_name(self, name):
        for payload in self:
            if payload.name == name:
                return payload
        return None
    
    def get_payloads_id(self):
        id_list = []
        for payload in self:
                id_list.append(str(payload.id))
        return id_list

    def register_payload(self, sourcepath, destinationname):
        
        newpayload = PayloadClass()
        newpayload.name = os.path.basename(sourcepath)
        newpayload.id = destinationname
        newpayload.sourcepath = sourcepath
        newpayload.url = gconfig.DNS_NAME + gconfig.BASE_PAYLOAD_URL + newpayload.id
        newpayload.storepath = "./payloadhosting/" + newpayload.id

        # Copy payload
        shutil.copyfile(newpayload.sourcepath, "./payloadhosting/"+newpayload.id) 
        #Add to payload list
        self.append(newpayload)
    
    def remove_payload(self, selected_payload):
        os.remove(selected_payload.storepath)
        self.remove(selected_payload)

class PayloadClass:
    def __init__(self):
        self.id = None
        self.name = None
        self.sourcepath = None
        

    def generate_payload(self):
        shutil.copyfile(self.sourcepath, "./payloadhosting/"+self.id)        
    
  