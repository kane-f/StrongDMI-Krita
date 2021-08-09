from krita import *

class StrongDMI(Extension):
    from .load import loadDMI
    from .save import saveDMI

    def __init__(self, parent):
        super().__init__(parent)

    # Krita.instance() exists, so do any setup work
    def setup(self):
        pass

    # called after setup(self)
    def createActions(self, window):
        action1 = window.createAction("load_dmi", "Load DMI file", "tools/scripts")
        #action1.triggered.connect(self.loadDMI("/"))
        action2 = window.createAction("save_dmi", "Save DMI file", "tools/scripts")
        #action2.triggered.connect(self.saveDMI("/"))
