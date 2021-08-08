from byond.DMI import DMI
from byond import directions
import krita

# File that handles saving the .dmi from layers and groups.

def saveDMI(file_path):
    doc = Krita.instance().openDocument(file_path)
    root = doc.rootNode()
