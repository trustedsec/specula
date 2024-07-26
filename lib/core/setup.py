from configparser import ConfigParser
from lib.validators.generic import *
from lib.validators.files import *
import os
import datetime
import random
import string

# to add a new setting Follow these steps
# 1 Add a @property and @<propname>.setter, follow format of existing options
# 2 add an entry into _setup setting your property / providing an optional default
# 3 add your setting to output in specula's do_settings command in specula.py
# 4 if special actions need to occur when this setting is updated on the fly, modify do_updateSettings in specula.py

def isdate(value):
    if value == "NONE":
        return True
    else:
        try:
            year, month, day = value.split('/')
            datetime.date(int(year), int(month), int(day)) # no exceptions, cool
            return True
        except Exception as msg:
            print("Invalid date, please use NONE to disable EndDate or enter a day in the format of year/month/day")
            return False


class Config:
    def __init__(self, configpath):
        self._config = None
        self.DEBUG=False
        self._configpath = configpath
        if not os.access(configpath, os.R_OK):
            print("A config file was not found at path {}\nStarting initial setup".format(configpath))
            self._setup()
        else:
            self._config = ConfigParser(interpolation=None)
            self._config.read('specConfig.ini')


    '''Attempts to get an option
    msg is the string to prompt the user with
    validator is an optional function to be called to validate, return True if valid, else false
    if value is set, our first attempt should not prompt'''
    @staticmethod
    def _getopt(msg, validator=None, value=None):
        opt = input(msg + ': ') if value is None else value
        while opt == "" or False if validator is None else not validator(opt):
            print('Input is invalid, please try again')
            opt = input(msg + ': ')
        return opt

    def _setup(self):
        self._config = ConfigParser(interpolation=None)
        self._config['DEFAULT'] = {}
        print("Pressing ENTER will set the default option")
        self.DNS_NAME = None
        self.PUSHOVER_API_TOKEN = input("Please specify your pushover.net user api token (Not app token!) or NONE if you do not want notifications(default:NONE): ") or "NONE"
        self.PUSHOVER_APP_API_TOKEN = input("Please specify your pushover.net app api token or NONE if you do not want notifications(default:NONE): ") or "NONE"
        self.END_DATE = input("Enter end date in the format of Year/Month/Day (Agent terminates after this date) or NONE if you do not want an end date(default:NONE): ") or "NONE"
        self.VALIDATE_URL = input("What url do you want for validation?(default:/plugin/search/): ") or "/plugin/search/"
        self.BASE_PATH_AGENT_COM = input("What should be used for the base agent coms path(default:/css/): ") or "/css/"
        self.BASE_PAYLOAD_URL = input("What should be used for base payload hosting(default:/random[10]/): ") or ''.join(random.choices(string.ascii_letters + string.digits, k=10))+"/"
        self.OUTLOOK_VIEW_ID = "SpeculaViewID"
        self.TIME_FORMAT = input('What time format should be used in logs(default:%m/%d/%Y-%H:%M:%S): ') or '%m/%d/%Y-%H:%M:%S'
        self.INITIAL_CHECKIN_COUNT = input("How many checkins to approve an agent, 0 for manual approval(default:5): ") or "5"
        self.REDIRECT_FALSE_AGENTS = input("Where should we send invalid agents? Either a url (https://www.outlook.com) or the word template (default:template): ") or "template"
        self.DEFAULT_REFRESH_TIME = input("Default agent refresh time in seconds(default:120): ") or "120"
        self.JITTER = input("Please set a max jitter value in seconds(default:30): ") or "30"
        self.CLSID = '0006F063-0000-0000-C000-000000000046'
        self.SPECULA_LOG_FILE = input('What should be our operational log file(default:specula_log.txt): ') or 'specula_log.txt'
        self.OPERATOR_LOG_FILE = input('What should be our operator log file(default:operator_log.txt): ') or 'operator_log.txt'
        self.SERVER_HEADER = input("What should we use for a server header(default:Microsoft-IIS/8.5): ") or 'Microsoft-IIS/8.5'
        self.ENCRYPTIONKEY_REGISTRY_LOCATION = input("In what key should the encryption value be stored on the client (Hive is always HKCU - default:SOFTWARE\\Microsoft\\Office\\<VERSION>\\Outlook\\UserInfo): ") or "DEFAULT"
        self.ENCRYPTIONKEY_VALUENAME = input("In what value name under the previous specified key location should the encryptionkey be stored (default:KEY): ") or "KEY"
        self.DATABASEFILENAME = "agents.db"
        self.PAYLOADFILENAME = "payloads.db"
        if self.DNS_NAME.startswith('https'): #auto set to true or false based on DNS_NAME
            self.SSL = "True"
        else:
            self.SSL = "false"
        if self.SSL:
            self.CERT_FILE = input("Path to server cert (default:./ssl/ssl-cert-snakeoil.pem): ") or './ssl/ssl-cert-snakeoil.pem'
            self.KEY_FILE = input("Path to server key (default:./ssl/ssl-cert-snakeoil.key): ") or './ssl/ssl-cert-snakeoil.key'
            self.WEBSERVER_PORT = input("What port should webserver listen on (default:443): ") or '443'
        else:
            self.CERT_FILE = ""
            self.KEY_FILE = ""
            self.WEBSERVER_PORT = input("What port should webserver listen on (default:80): ") or '80'
        self.IP_blocklist = input("Please specify a file to use for blocklists(Defaultblocklist.txt) or NONE to not use blocklisting(default:NONE): ") or "NONE"
        # Subscription config
        self.PUSH_VALIDATION = "True"
        self.PUSH_NEWAGENT = "True"
        self.PUSH_NEWIP = "True"
        self.PUSH_UNEXPECTEDCALLBACK = "True"
        self.PUSH_UNKNOWNCONNECTION = "True"
        self.PUSH_PRESTAGE = "True"
        self.PUSH_CONNECTION_OUTSIDESPECULA = "False"

    def _save_config(self):
        with open(self._configpath, 'w') as fp:
            self._config.write(fp)

    @property
    def PUSHOVER_API_TOKEN(self):
        return self._config['DEFAULT']['PUSHOVER_API_TOKEN'] if self._config['DEFAULT']['PUSHOVER_API_TOKEN'] != "NONE" else None

    @PUSHOVER_API_TOKEN.setter
    def PUSHOVER_API_TOKEN(self, value):
        opt = self._getopt("specify your pushover.net user api token or NONE if you do not want notifications", value=value)
        if opt.upper() == "NONE":
            opt = "NONE"
        self._config['DEFAULT']['PUSHOVER_API_TOKEN'] = opt
        self._save_config()

    @property
    def PUSHOVER_APP_API_TOKEN(self):
        return self._config['DEFAULT']['PUSHOVER_APP_API_TOKEN'] if self._config['DEFAULT']['PUSHOVER_APP_API_TOKEN'] != "NONE" else None

    @PUSHOVER_APP_API_TOKEN.setter
    def PUSHOVER_APP_API_TOKEN(self, value):
        opt = self._getopt("specify your pushover.net app api token or NONE if you do not want notifications", value=value)
        if opt.upper() == "NONE":
            opt = "NONE"
        self._config['DEFAULT']['PUSHOVER_APP_API_TOKEN'] = opt
        self._save_config()

    @property
    def TIME_FORMAT(self):
        return self._config['DEFAULT']['TIME_FORMAT']

    @TIME_FORMAT.setter #some kind of validator should probably go on here...
    def TIME_FORMAT(self, value):
        self._config['DEFAULT']['TIME_FORMAT'] = value
        self._save_config()

    @property
    def DNS_NAME(self):
        return self._config['DEFAULT']['DNS_NAME']

    @DNS_NAME.setter
    def DNS_NAME(self, value):
        self._config['DEFAULT']['DNS_NAME'] = self._getopt("Please provide a fully qualified dns name (example:http://evil.com)",
                                                           validator=iswebaddress, value=value)
        self._save_config()

    @property
    def INITIAL_CHECKIN_COUNT(self):
        return int(self._config['DEFAULT']['INITIAL_CHECKIN_COUNT'])

    @INITIAL_CHECKIN_COUNT.setter
    def INITIAL_CHECKIN_COUNT(self,value):
        self._config['DEFAULT']['INITIAL_CHECKIN_COUNT'] = self._getopt("How many checkings to authenticate an agent (use 0 for manual approval)",
                                                                        validator=isint, value=value)
        self._save_config()

    @property
    def VALIDATE_URL(self):
        return self._config['DEFAULT']['VALIDATE_URL']

    @VALIDATE_URL.setter
    def VALIDATE_URL(self, value):
        opt  = self._getopt("please define a path for the validate url", value=value)
        if opt[0] != '/':
            opt = '/' + opt
        self._config['DEFAULT']['VALIDATE_URL'] = opt
        self._save_config()

    @property
    def BASE_PATH_AGENT_COM(self):
        return self._config['DEFAULT']['BASE_PATH_AGENT_COM']

    @BASE_PATH_AGENT_COM.setter
    def BASE_PATH_AGENT_COM(self, value):
        opt  = self._getopt("please define a base path used for agent urls / comms", value=value)
        if opt[0] != '/':
            opt = '/' + opt
        self._config['DEFAULT']['BASE_PATH_AGENT_COM'] = opt
        self._save_config()
    
    @property
    def BASE_PAYLOAD_URL(self):
        return self._config['DEFAULT']['BASE_PAYLOAD_URL']

    @BASE_PAYLOAD_URL.setter
    def BASE_PAYLOAD_URL(self, value):
        opt  = self._getopt("please define a base path used for hosting payloads", value=value)
        if opt[0] != '/':
            opt = '/' + opt
        self._config['DEFAULT']['BASE_PAYLOAD_URL'] = opt
        self._save_config()

    @property
    def REDIRECT_FALSE_AGENTS(self):
        return self._config['DEFAULT']['REDIRECT_FALSE_AGENTS']

    @REDIRECT_FALSE_AGENTS.setter
    def REDIRECT_FALSE_AGENTS(self, value):
        self._config['DEFAULT']['REDIRECT_FALSE_AGENTS'] = self._getopt('Where should we send Blocked and invalid agents',
                                                                        value=value)
        self._save_config()

    @property
    def ENCRYPTIONKEY_VALUENAME(self):
        return self._config['DEFAULT']['ENCRYPTIONKEY_VALUENAME']

    @ENCRYPTIONKEY_VALUENAME.setter
    def ENCRYPTIONKEY_VALUENAME(self, value):
        self._config['DEFAULT']['ENCRYPTIONKEY_VALUENAME'] = self._getopt('What should the encryptionkey name in the registry be', value=value)
        self._config['DEFAULT']['ENCRYPTIONKEY_VALUENAME'] = "\"" + self._config['DEFAULT']['ENCRYPTIONKEY_VALUENAME'] + "\""
        self._save_config()

    @property
    def ENCRYPTIONKEY_REGISTRY_LOCATION(self):
        return self._config['DEFAULT']['ENCRYPTIONKEY_REGISTRY_LOCATION']

    @ENCRYPTIONKEY_REGISTRY_LOCATION.setter
    def ENCRYPTIONKEY_REGISTRY_LOCATION(self, value):
        self._config['DEFAULT']['ENCRYPTIONKEY_REGISTRY_LOCATION'] = self._getopt('Where should the encryption key be stored on the client', value=value)
        if self._config['DEFAULT']['ENCRYPTIONKEY_REGISTRY_LOCATION'] == "DEFAULT":
            self._config['DEFAULT']['ENCRYPTIONKEY_REGISTRY_LOCATION'] = "\"Software\\Microsoft\\Office\\\"  & Left(outlookapp.version,4) & \"\\Outlook\\UserInfo\""
        else:
            self._config['DEFAULT']['ENCRYPTIONKEY_REGISTRY_LOCATION'] = "\"" + self._config['DEFAULT']['ENCRYPTIONKEY_REGISTRY_LOCATION'] + "\""
        self._save_config()


    @property
    def DEFAULT_REFRESH_TIME(self):
        return self._config['DEFAULT']['DEFAULT_REFRESH_TIME']#used as a string which is why we don't int convert

    @DEFAULT_REFRESH_TIME.setter
    def DEFAULT_REFRESH_TIME(self,value):
        self._config['DEFAULT']['DEFAULT_REFRESH_TIME'] = self._getopt("Default agent refresh time in seconds",
                                                                       validator=isint, value=value)
        self._save_config()

    @property
    def SPECULA_LOG_FILE(self):
        return self._config['DEFAULT']['specula_log_file']

    @SPECULA_LOG_FILE.setter
    def SPECULA_LOG_FILE(self,value):
        self._config['DEFAULT']['SPECULA_LOG_FILE'] = self._getopt("Where should specula log operational messages",
                                                                   value=value)
        self._save_config()

    @property
    def OPERATOR_LOG_FILE(self):
        return self._config['DEFAULT']['OPERATOR_LOG_FILE']

    @OPERATOR_LOG_FILE.setter
    def OPERATOR_LOG_FILE(self,value):
        self._config['DEFAULT']['OPERATOR_LOG_FILE'] = self._getopt("Where should operator log operational messages",
                                                                   value=value)
        self._save_config()

    @property
    def SERVER_HEADER(self):
        return self._config['DEFAULT']['SERVER_HEADER']

    @SERVER_HEADER.setter
    def SERVER_HEADER(self, value):
        self._config['DEFAULT']['SERVER_HEADER'] = self._getopt("What should this server identify itself as",
                                                                value=value)
        self._save_config()

    @property
    def OUTLOOK_VIEW_ID(self):
        return self._config['DEFAULT']['OUTLOOK_VIEW_ID']

    @OUTLOOK_VIEW_ID.setter
    def OUTLOOK_VIEW_ID(self, value):
        self._config['DEFAULT']['OUTLOOK_VIEW_ID'] = self._getopt("What should outlook use as a view id",
                                                                  value=value)
        self._save_config()

    @property
    def CLSID(self):
        return self._config['DEFAULT']['CLSID']

    @CLSID.setter
    def CLSID(self, value):
        self._config['DEFAULT']['CLSID'] = self._getopt("What CLSID should HTML use when rendering",
                                                                  value=value)
        self._save_config()

    @property
    def DATABASEFILENAME(self):
        return self._config['DEFAULT']['DATABASEFILENAME']

    @DATABASEFILENAME.setter
    def DATABASEFILENAME(self,value):
        self._config['DEFAULT']['DATABASEFILENAME'] = self._getopt("Filename for agents database",
                                                                   value=value)
        self._save_config()

    @property
    def PAYLOADFILENAME(self):
        return self._config['DEFAULT']['PAYLOADFILENAME']

    @PAYLOADFILENAME.setter
    def PAYLOADFILENAME(self,value):
        self._config['DEFAULT']['PAYLOADFILENAME'] = self._getopt("Filename for payloads database",
                                                                   value=value)
        self._save_config()

    @property
    def SSL(self):
        return bool(self._config['DEFAULT']['SSL'])

    @SSL.setter
    def SSL(self, value):
        self._config['DEFAULT']['SSL'] = "" if self._getopt("Should we use SSL(True/False)", validator=isboolstring,
                                                            value=value).lower() == "false" else "True"
        self._save_config()


    @property
    def CERT_FILE(self):
        return "" if self.SSL is False else self._config['DEFAULT']['CERT_FILE']

    @CERT_FILE.setter
    def CERT_FILE(self,value):
        self._config['DEFAULT']['CERT_FILE'] = value if value == "" else \
            self._getopt("path to server cert", validator=isreadable, value=value)
        self._save_config()

    @property
    def KEY_FILE(self):
        return "" if self.SSL is False else self._config['DEFAULT']['KEY_FILE']

    @KEY_FILE.setter
    def KEY_FILE(self,value):
        self._config['DEFAULT']['KEY_FILE'] = value if value == "" else\
            self._getopt("path to server key", validator=isreadable, value=value)
        self._save_config()

    @property
    def JITTER(self):
        return self._config['DEFAULT']['JITTER']

    @JITTER.setter
    def JITTER(self, value):
        self._config['DEFAULT']['JITTER'] = self._getopt("Please set a max jitter value in seconds",
                                                         validator=isint, value=value)
        self._save_config()

    @property
    def IP_blocklist(self):
        return self._config['DEFAULT']['IP_blocklist'] if self._config['DEFAULT']['IP_blocklist'] != "NONE" else None

    @IP_blocklist.setter
    def IP_blocklist(self, value):
        self._config['DEFAULT']['IP_blocklist'] = self._getopt("Please specify a file to use for blocklists, NONE to disable",value=value)
        self._save_config()

    @property
    def END_DATE(self):
        if self._config['DEFAULT']['END_DATE'] == "NONE":
            return None
        else:
            y, m, d = self._config['DEFAULT']['END_DATE'].split('/')
            return datetime.date(int(y), int(m), int(d))

    @END_DATE.setter
    def END_DATE(self, value):
        self._config['DEFAULT']['END_DATE'] = self._getopt("Enter end date in the format of Year/Month/Day (Agent terminates after this date) or NONE",
                                                           validator=isdate,
                                                           value=value)
        self._save_config()

    @property
    def WEBSERVER_PORT(self):
        return int(self._config['DEFAULT']['WEBSERVER_PORT'])

    @WEBSERVER_PORT.setter
    def WEBSERVER_PORT(self,value):
        self._config['DEFAULT']['WEBSERVER_PORT'] = self._getopt("What port should the webserver listen on?",
                                                                        validator=isint, value=value)
        self._save_config()

    @property
    def PUSH_VALIDATION(self):
        return (self._config['DEFAULT']['PUSH_VALIDATION'])

    @PUSH_VALIDATION.setter
    def PUSH_VALIDATION(self, value):
        if value.lower() == "true":
            self._config['DEFAULT']['PUSH_VALIDATION'] = "True"
        else:
            self._config['DEFAULT']['PUSH_VALIDATION'] = "False"
        self._save_config()

    @property
    def PUSH_NEWAGENT(self):
        return (self._config['DEFAULT']['PUSH_NEWAGENT'])

    @PUSH_NEWAGENT.setter
    def PUSH_NEWAGENT(self, value):
        if value.lower() == "true":
            self._config['DEFAULT']['PUSH_NEWAGENT'] = "True"
        else:
            self._config['DEFAULT']['PUSH_NEWAGENT'] = "False"
        self._save_config()

    @property
    def PUSH_NEWIP(self):
        return (self._config['DEFAULT']['PUSH_NEWIP'])

    @PUSH_NEWIP.setter
    def PUSH_NEWIP(self, value):
        if value.lower() == "true":
            self._config['DEFAULT']['PUSH_NEWIP'] = "True"
        else:
            self._config['DEFAULT']['PUSH_NEWIP'] = "False"
        self._save_config()  

    @property
    def PUSH_UNEXPECTEDCALLBACK(self):
        return (self._config['DEFAULT']['PUSH_UNEXPECTEDCALLBACK'])

    @PUSH_UNEXPECTEDCALLBACK.setter
    def PUSH_UNEXPECTEDCALLBACK(self, value):
        if value.lower() == "true":
            self._config['DEFAULT']['PUSH_UNEXPECTEDCALLBACK'] = "True"
        else:
            self._config['DEFAULT']['PUSH_UNEXPECTEDCALLBACK'] = "False"
        self._save_config()  

    @property
    def PUSH_UNKNOWNCONNECTION(self):
        return (self._config['DEFAULT']['PUSH_UNKNOWNCONNECTION'])

    @PUSH_UNKNOWNCONNECTION.setter
    def PUSH_UNKNOWNCONNECTION(self, value):
        if value.lower() == "true":
            self._config['DEFAULT']['PUSH_UNKNOWNCONNECTION'] = "True"
        else:
            self._config['DEFAULT']['PUSH_UNKNOWNCONNECTION'] = "False"
        self._save_config()

    @property
    def PUSH_PRESTAGE(self):
        return (self._config['DEFAULT']['PUSH_PRESTAGE'])

    @PUSH_PRESTAGE.setter
    def PUSH_PRESTAGE(self, value):
        if value.lower() == "true":
            self._config['DEFAULT']['PUSH_PRESTAGE'] = "True"
        else:
            self._config['DEFAULT']['PUSH_PRESTAGE'] = "False"
        self._save_config()

    @property
    def PUSH_CONNECTION_OUTSIDESPECULA(self):
        return (self._config['DEFAULT']['PUSH_CONNECTION_OUTSIDESPECULA'])

    @PUSH_CONNECTION_OUTSIDESPECULA.setter
    def PUSH_CONNECTION_OUTSIDESPECULA(self, value):
        if value.lower() == "true":
            self._config['DEFAULT']['PUSH_CONNECTION_OUTSIDESPECULA'] = "True"
        else:
            self._config['DEFAULT']['PUSH_CONNECTION_OUTSIDESPECULA'] = "False"
        self._save_config()  

gconfig = Config('specConfig.ini')






    









