from PIL import Image
import io
from byond.DMI import DMI
from byond import directions
import krita

# File that handles saving the .dmi from layers and groups.

def saveDMI(file_path):
    dmi = DMI()
    doc = Krita.instance().openDocument(file_path)
    root = doc.rootNode()
    
    for state_node in root.childNodes():
        if state_node.type() == "paintlayer":
            current_icon = Image.open(io.BytesIO(state_node.pixelData(0,0,doc.width(),doc.height())))
        elif state_node.type() == "grouplayer":
            for dir_node in state_node.childNodes():
                if dir_node.type() == "paintlayer":
                    current_icon = Image.open(io.BytesIO(state_node.pixelData(0,0,doc.width(),doc.height())))
                elif dir_node.type() == "grouplayer":
                    for frame_node in dir_node.childNodes():
                        if frame_node.type() == "paintlayer":
                            current_icon = Image.open(io.BytesIO(state_node.pixelData(0,0,doc.width(),doc.height())))
