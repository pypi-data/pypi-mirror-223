from ciocore import data as coredata
from ciokatana.v1 import const as k

INSTANCE_TYPE_PARAM = "instanceType"
PREEMPTIBLE_PARAM = "preemptible"
RETRIES_PARAM = "retries"


def create(node):
    """Create the parameters.
    
    To choose the initial instance_type, we look for the first instance type
    with more than 2 cores and more than 8GB of memory. If none is found, we
    just use the first one we find.
    """

    instance_type = _capable_instance_type_name()
    node.getParameters().createChildString(INSTANCE_TYPE_PARAM, instance_type)
    node.getParameters().createChildNumber(PREEMPTIBLE_PARAM, 1)
    node.getParameters().createChildNumber(RETRIES_PARAM, 1)

def set_value(node, value):
    node.getParameter(INSTANCE_TYPE_PARAM).setValue(value, 0)

def get_value(node):
    hardware = coredata.data()["instance_types"] if coredata.valid() else None
    value = node.getParameter(INSTANCE_TYPE_PARAM).getValue(0)
    if not hardware.find(value):
        value = _capable_instance_type_name()
    set_value(node, value)
    return value
    
def resolve(node):
    """Resolve the payload for the node."""
    result = {
        "instance_type": get_value(node),
        "preemptible": node.getParameter(PREEMPTIBLE_PARAM).getValue(0) > 0,
    }
    retries =  int(node.getParameter(RETRIES_PARAM).getValue(0))
    if result["preemptible"] and retries:
        result.update({"autoretry_policy": {"preempted": {"max_retries": retries}}})
    return result

def _capable_instance_type_name():
    """Find the first instance type with more than 2 cores and more than 8GB of memory.
    
    If none is found, just use the first one we find.
    """
    hardware = coredata.data()["instance_types"] if coredata.valid() else None
    
    if not hardware:
        return k.NOT_CONNECTED
    result = hardware.find_first( lambda x: float(x["cores"]) > 2 and float(x["memory"]) > 8 )
    if result:
        return result["name"]
    return hardware.find_first( lambda x: True )["name"]