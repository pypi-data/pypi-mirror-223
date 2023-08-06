"""
NAME: ReloadConductorFlush
ICON: icon.png
KEYBOARD_SHORTCUT: 
SCOPE:
Reload Conductor Flush

"""

import importlib
from Katana import NodegraphAPI
from ciokatana.v1 import reloader
importlib.reload(reloader)

crnode = NodegraphAPI.GetNode('ConductorRender')
if crnode:
    crnode.delete()
    
    
reloader.reload()
console_print("reloaded")