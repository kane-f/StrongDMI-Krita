from byond.DMI import DMI
from byond import directions
import krita

# File that handles saving the .dmi from layers and groups.

def saveDMI(file_path):
    doc = Krita.instance().openDocument(file_path)
    root = doc.rootNode()
    
    for state_node in root.childNodes():
        if state_node.type() == "paintlayer":
        elif state_node.type() == "grouplayer":
            for dir_node in state_node.childNodes():
                if state_node.type() == "paintlayer":
                elif state_node.type() == "grouplayer":
                    for frame_node in dir_node.childNodes():
                        if state_node.type() == "paintlayer":
