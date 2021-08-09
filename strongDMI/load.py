from byond.DMI import DMI
from byond import directions
import krita

# File that handles loading the .dmi and splitting it into layers and groups.
# TODO: Add keyframe support whenever Krita's python API fully supports it, will look much less painstaking than layers and was the original idea. Also remove deprecated division thing.

def loadDMI(file_path):
    dmi = DMI(file_path)
    dmi.loadAll()
        
    doc = Krita.instance().openDocument(file_path)
    root = doc.rootNode()
    bg_node = doc.nodeByName("background")
    assert bg_node # So we don't open a non-existant layer (not that it is, it always loads as "background")

    i = 0 #iterator
    for state_name in dmi.states:
        current_state = dmi.states[state_name]
        if current_state.dirs == 1: # Only one dir
            if current_state.frames == 1:
                state_x = dmi.icon_width * (i % (doc.width() / dmi.icon_width)) # Along rows
                state_y = dmi.icon_height * (i // (doc.width() / dmi.icon_width)) # Along columns
                current_icon = bg_node.pixelData(state_x,state_y,dmi.icon_width,dmi.icon_height) # Grab this section from the base image, use set width/height in .dmi
                state_node = doc.createNode(state_name,"paintLayer") # Paint layers for nothing else to do, top level is state name
                root.addChildNode(state_node, None)
                state_node.setPixelData(current_icon,0,0,dmi.icon_width,dmi.icon_height) # And placing it inside the layer
                state_node.setVisible(False) # QoL stuff so the loaded result isn't a cloudy blur of icons
                i += 1 # Iterate when done
            else: # More than one frame, an animation
                state_node = doc.createNode(state_name,"groupLayer") # Groups for sub-layers with more to do
                root.addChildNode(state_node, None)
                for frame in range(current_state.frames): # Iterate over frames and display under
                    state_x = dmi.icon_width * (i % (doc.width() / dmi.icon_width))
                    state_y = dmi.icon_height * (i // (doc.width() / dmi.icon_width))
                    current_icon = bg_node.pixelData(state_x,state_y,dmi.icon_width,dmi.icon_height)
                    frame_node = doc.createNode(str(current_state.delay[frame]),"paintLayer") # Delay of frame is used as layer name in lieue of Krita having fixed framerates
                    state_node.addChildNode(frame_node, None)
                    frame_node.setPixelData(current_icon,0,0,dmi.icon_width,dmi.icon_height)
                    frame_node.setVisible(False)
                    i += 1
                state_node.setCollapsed(True) # Collapse group nodes, more QoL for browsing purposes
        else: # 4 or 8 dirs
            state_node = doc.createNode(state_name,"groupLayer")
            root.addChildNode(state_node, None)
            for direction in range(current_state.dirs): # Iterate over "directions"
                dirf = directions.IMAGE_INDICES[direction] # Convert these to proper indices, shameless taken from BYONDTools code itself somewhere
                dirn = directions.getNameFromDir(dirf) # Makes them readable (because confusing them with frame delays would be baaad)
                if current_state.frames == 1:
                    state_x = dmi.icon_width * (i % (doc.width() / dmi.icon_width))
                    state_y = dmi.icon_height * (i // (doc.width() / dmi.icon_width))
                    current_icon = bg_node.pixelData(state_x,state_y,dmi.icon_width,dmi.icon_height)
                    dir_node = doc.createNode(dirn,"paintLayer") # Setting direction name as layer name
                    state_node.addChildNode(dir_node, None)
                    dir_node.setPixelData(current_icon,0,0,dmi.icon_width,dmi.icon_height)
                    dir_node.setVisible(False)
                    i += 1
                else:
                    dir_node = doc.createNode(dirn,"groupLayer")
                    state_node.addChildNode(dir_node, None)
                    for frame in range(current_state.frames):
                        state_x = dmi.icon_width * (i % (doc.width() / dmi.icon_width))
                        state_y = dmi.icon_height * (i // (doc.width() / dmi.icon_width))
                        current_icon = bg_node.pixelData(state_x,state_y,dmi.icon_width,dmi.icon_height)
                        frame_node = doc.createNode(str(current_state.delay[frame]),"paintLayer")
                        dir_node.addChildNode(frame_node, None)
                        frame_node.setPixelData(current_icon,0,0,dmi.icon_width,dmi.icon_height)
                        frame_node.setVisible(False)
                        i += 1
                dir_node.setCollapsed(True)
            state_node.setCollapsed(True)

    doc.setWidth(dmi.icon_width) # When processing is done, resize document
    doc.setHeight(dmi.icon_height)
    root.removeChildNode(bg_node) # Get rid of the background we used
    Krita.instance().activeWindow().addView(doc) # Finally, show the user our work
