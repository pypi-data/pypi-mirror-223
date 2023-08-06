from ciocore import data as coredata
from ciokatana.v1 import const as k

PROJECT_PARAM = "conductorProject"

def create(node):
    """Create the project parameter on the node.
    
    If we already connected to conductor, use the first project in the list.
    """
    projects = coredata.data()["projects"] if coredata.valid() else []
    
    if projects:
        project = projects[0]
    else:
        project = k.NOT_CONNECTED
    node.getParameters().createChildString(PROJECT_PARAM, project)

# accessors
def get_value(node):
    """Getter ensures that the value is valid, or easy to spot if not."""
    projects = coredata.data()["projects"] if coredata.valid() else []
    value = node.getParameter(PROJECT_PARAM).getValue(0)
    if value in projects:
        return value
    if "default" in projects:
        value="default"
    elif projects:
        value = projects[0]
    else:
        value = k.NOT_CONNECTED
    
    set_value(node, value)
    return value

def set_value(node, value):
    node.getParameter(PROJECT_PARAM).setValue(value, 0)

def resolve(node):
    """Resolve the payload field for the project parameter."""
    return {"project": get_value(node)}
