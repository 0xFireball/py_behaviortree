import sys
sys.path.append('../src')

from behaviortree.behavior import Status

def parse_executing(call_chain):
    executing = []
    for node in call_chain:
        # check node type
        is_composite = hasattr(node, "_children")
        is_decorator = hasattr(node, "_child")
        if not is_composite and not is_decorator:
            executing.append(node)
    return executing

def crunch_status(status: Status):
    if status == status.SUCCESS:
        return 'S'
    if status == status.FAILURE:
        return 'F'
    if status == status.RUNNING:
        return 'R'
    return status