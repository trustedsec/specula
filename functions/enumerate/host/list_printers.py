from lib.core.specmodule import SpecModule
from datetime import datetime

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Uses wscript.network to gather printer connections

        It uses Wscript.Network
        - EnumPrinterConnections
        """
        self.entry = 'list_printers'
        self.depends = []
        super().__init__(templatepath)
