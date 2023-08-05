def register(pool, entries, entry_point_type="Node"):
    for entry in entries:
        if entry.identifier not in pool:
            pool[entry.identifier] = entry
        else:
            raise Exception(
                "{} {} is already registered.".format(
                    entry_point_type, entry.identifier
                )
            )


# load entry points
def get_entries(entry_point_name, entry_point_type="Node"):
    from importlib.metadata import entry_points

    pool = {}
    for entry_point in entry_points().get(entry_point_name, []):
        new_entries = entry_point.load()
        register(pool, new_entries, entry_point_type)
    return pool


def get_time(total_seonds):
    d = divmod(total_seonds, 86400)  # days
    h = divmod(d[1], 3600)  # hours
    m = divmod(h[1], 60)  # minutes
    # s = m[1]  # seconds
    t = "{:d}d-{:d}h-{:d}m".format(d[0], h[0], m[0])
    return t


def load_nodetree(uuid):
    from scinode import NodeTree

    nt = NodeTree.load(uuid)
    return nt


def load_node(uuid):
    from scinode.core.node import Node

    node = Node.load(uuid)
    return node


def load_yaml(filename=None, string=None):
    import yaml

    # load data
    if filename:
        with open(filename, "r") as f:
            data = yaml.safe_load(f)
    elif string:
        data = yaml.safe_load(string)
    else:
        raise Exception("Please specific a filename or yaml string.")
    return data


def get_ctx(dbdata):
    """Get context for node execution.

    Args:
        dbdata (dict): node data from database

    Returns:
        dict: workdir, node_uuid, nodetree_uuid
    """
    from scinode.daemon.worker_config import WorkerConfig

    worker = WorkerConfig(name=dbdata["metadata"]["worker_name"])
    data = worker.data
    ctx = {
        "workdir": data["workdir"],
        "node_uuid": dbdata["uuid"],
        "nodetree_uuid": dbdata["metadata"]["nodetree_uuid"],
    }
    return ctx


def load_module(path):
    import importlib

    data = path.rsplit(".", 1)
    module = importlib.import_module("{}".format(data[0]))
    _ = getattr(module, data[1])
