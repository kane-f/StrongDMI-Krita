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
    
    i = 0
    for state_node in root.childNodes():
        if state_node.type() == "paintlayer":
            current_icon = Image.open(io.BytesIO(state_node.pixelData(0,0,doc.width(),doc.height())))
            dmi.states[state_node.name()] = DMIState(state_node.name())
            dmi.states[state_node.name()].frames = 0
            dmi.states[state_node.name()].dirs = 1
            dmi.states[state_node.name()].icons[i] = current_icon
            i += 1
        elif state_node.type() == "grouplayer":
            for dir_node in state_node.childNodes():
                if dir_node.type() == "paintlayer":
                    current_icon = Image.open(io.BytesIO(state_node.pixelData(0,0,doc.width(),doc.height())))
                    dmi.states[state_node.name()] = DMIState(state_node.name())
                    dmi.states[state_node.name()].frames = len(state_node.childNodes())
                    dmi.states[state_node.name()].dirs = 1
                    dmi.states[state_node.name()].icons[i] = current_icon
                    i += 1
                elif dir_node.type() == "grouplayer":
                    for frame_node in dir_node.childNodes():
                        if frame_node.type() == "paintlayer":
                            current_icon = Image.open(io.BytesIO(state_node.pixelData(0,0,doc.width(),doc.height())))
                            dmi.states[state_node.name()] = DMIState(state_node.name())
                            dmi.states[state_node.name()].frames = len(dir_node.childNodes())
                            dmi.states[state_node.name()].dirs = len(state_node.childNodes())
                            dmi.states[state_node.name()].icons[i] = current_icon
                            dmi.states[state_node.name()].delay[i] = frame_node.name()
                            i += 1
                            
    dmi.icon_width = doc.width()
    dmi.icon_height = doc.height()
    dmi.save(file_path)
