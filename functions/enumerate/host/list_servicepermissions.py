from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the services and the permissions on the host. 

        It lists out:
        - Service Name
        - Service Binary path
        - Group name and Access
        
        Example Output:        
        Enumerating Permissions for: UserDataSvc_3dc16
        C:\Windows\system32\svchost.exe
            GROUP: NT SERVICE\TRUSTEDINSTALLER
                binPath: C:\Windows\system32\svchost.exe
                Sanity Check - Access Mask Value To Match: 2032127
                    ACE Type: Allow
                    Access Mask (Decimal): 2032127 (FullControl)
        
        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select * from Win32_Service
        - Query: Select * from win32_logicalFileSecuritySetting WHERE Path=VARIABLE
        """        
        self.entry = 'list_servicepermissions'
        self.depends = []
        super().__init__(templatepath)
        