from PIL import Image
from byond.DMI import DMI, State
from byond import directions
import krita

# File that handles saving the .dmi from layers and groups.
# TODO: Write more stuff in and out, keep full compatiability.

def saveDMI(self, file_path):
    dmi = DMI("tmp.dmi") # To get around file not found issues
    doc = Krita.instance().activeDocument()
    assert doc # Make sure a doc is open
    root = doc.rootNode()
    
    for state_node in root.childNodes():
        dmi.states[state_node.name()] = State(state_node.name()) # Make new state object up here, including name
        if state_node.type() == "paintlayer": # If node is paint layer
            current_icon = Image.frombytes("RGBA",(doc.width(),doc.height()),state_node.pixelData(0,0,doc.width(),doc.height())) # Default krita mode, QByteArray loaded in (even suggested in docs!)
            dmi.states[state_node.name()].dirs = 1
            dmi.states[state_node.name()].icons += [current_icon] # Has to be in [] to be iterable
        elif state_node.type() == "grouplayer": # If node is group layer
            for dir_node in state_node.childNodes():
                if dir_node.type() == "paintlayer":
                    current_icon = Image.frombytes("RGBA",(doc.width(),doc.height()),state_node.pixelData(0,0,doc.width(),doc.height()))
                    dmi.states[state_node.name()].frames = len(state_node.childNodes()) # Frames is amount of layers under this group
                    dmi.states[state_node.name()].dirs = 1
                    dmi.states[state_node.name()].icons += [current_icon]
                    dmi.states[state_node.name()].delay += dir_node.name() # Layer names get converted to frame delay, much better system needed eventually
                elif dir_node.type() == "grouplayer":
                    for frame_node in dir_node.childNodes():
                        if frame_node.type() == "paintlayer":
                            current_icon = Image.frombytes("RGBA",(doc.width(),doc.height()),state_node.pixelData(0,0,doc.width(),doc.height()))
                            dmi.states[state_node.name()].frames = len(dir_node.childNodes())
                            dmi.states[state_node.name()].dirs = 8 if len(state_node.childNodes()) >= 8 else 4 # Directions are amount of layers under this group, truncated to 8 or 4
                            dmi.states[state_node.name()].icons += [current_icon]
                            dmi.states[state_node.name()].delay += frame_node.name()
                            
    dmi.icon_width = doc.width()
    dmi.icon_height = doc.height()
    dmi.save(file_path,sort=False)
