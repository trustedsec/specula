from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Executes the specified COM application hidden.
        Application is specified setting the com_application option. It defaults to word.application.
        Note that some of the applications starts and immmediatly terminates.

        Typical application are: 
        - word.application
        - excel.application
        - powerpoint.application
        - access.application
        - oneNote.application
        - publisher.application

        Full list of objects can be found using this Powershell oneliner:
        gci HKLM:\\Software\\Classes -ea 0| ? {$_.PSChildName -match '^\\w+\\.\\w+$' -and (gp "$($_.PSPath)\\CLSID" -ea 0)} | ft PSChildName

        The executed application gets the parent pid of SVCHost.exe (C:\Windows\system32\svchost.exe -k DcomLaunch -p)

        It uses CreateObject(Specified com application)
        """
        self.entry = 'Execute_Application'
        self.depends = []
        self.options['com_application'] = {
            "value": "word.application",
            "required": True,
            "description": "COM application to start",
            "handler": quotedstring
        }
        super().__init__(templatepath)
