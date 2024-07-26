from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.depends = ['./helperFunctions/dir_lister.txt']
        self.help = """
        Lists Group Policy Preferences files local on host that could contain passwords, configurations or other data.
        It looks inside C:\\Windows\\System32\\GroupPolicy\\DataStore\\0\\sysvol\\domain.com\\Policies\\ on the local host for the following files
        Groups.xml
        Drives.xml
        Services.xml
        ScheduledTasks.xml
        Datasources.xml
        Printers.xml

        It uses Wscript.Shell
        - ExpandEnvironmentStrings
        
        It uses Scripting.FileSystemObject
        - FolderExists
        - GetFolder
        - GetFolder().Files
        - GetBaseName
        - GetExtensionName
        """
        self.entry = 'list_gpp'
        self.depends = []
        super().__init__(templatepath)
        