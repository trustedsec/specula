from lib.core.specmodule import SpecModule


class SpecTaskBook(SpecModule):
    def __init__(self):
        self.entry = "None"
        self.depends = []
        super().__init__(None) # we inherit the base properties of a module


