import click
from scinode.orm.db_nodetree import DBNodeTree


@click.group(help="CLI tool to manage nodetree.")
def nodetree():
    pass


@nodetree.command(help="Launch nodetrees.")
@click.option("-n", "--name", help="Name of the item.")
@click.option("-i", "--index", help="Index of the item.", type=int)
@click.option("--state", help="State of the item.")
@click.option("--uuid", help="uuid of the item.")
@click.option("--action", help="Action of the item.")
def launch(name, index, uuid, state, action):
    from scinode.database.client import scinodedb

    query = {}
    if name:
        query["name"] = {"$regex": name}
    if index:
        query["index"] = index
    if uuid:
        query["uuid"] = uuid
    if state:
        query["state"] = state
    if action:
        query["action"] = action
    items = scinodedb["nodetree"].find(query, {"_id": 0, "name": 1, "uuid": 1})
    for item in items:
        nt = DBNodeTree(uuid=item["uuid"])
        nt.launch()
        click.secho(f'Launch nodetree: {item["name"]} successfully!', fg="green")


@nodetree.command(help="Reset nodetree.")
@click.option("--name", help="Name of the nodetree.")
@click.option("--index", help="Index of the nodetree.", type=int)
@click.option("--state", help="State of the nodetree.")
@click.option("--uuid", help="uuid of the nodetree.")
def reset(name, index, uuid, state):
    from scinode.database.client import scinodedb
    from scinode.engine.send_to_queue import reset_nodetree

    query = {}
    if name:
        query["name"] = {"$regex": name}
    if index:
        query["index"] = index
    if uuid:
        query["uuid"] = uuid
    if state:
        query["state"] = state
    items = scinodedb["nodetree"].find(
        query, {"_id": 0, "metadata.worker_name": 1, "uuid": 1, "name": 1}
    )
    if items is None:
        return
    for item in items:
        reset_nodetree(item["metadata"]["worker_name"], item["uuid"])
        click.secho(
            f'Send the message to reset nodetree: {item["name"]} successfully!',
            fg="green",
        )


@nodetree.command(help="List the nodetrees.")
@click.option("-n", "--name", help="Name of the item.")
@click.option("-i", "--index", help="Index of the item.", type=int)
@click.option("--uuid", help="uuid of the item.")
@click.option("--state", help="State of the item.")
@click.option("--action", help="Action of the item.")
@click.option("--worker", help="Worker used to run this node.")
@click.option("--limit", help="Limit of the item.", type=int, default=100)
def list(name, index, uuid, state, action, worker, limit):
    from scinode.database.nodetree import NodetreeClient

    client = NodetreeClient()
    query = {}
    if name:
        query["name"] = {"$regex": name}
    if index:
        query["index"] = index
    if uuid:
        query["uuid"] = uuid
    if state:
        query["state"] = state
    if action:
        query["action"] = action
    if worker:
        query["worker_name"] = worker
    client.list(query, limit)


@nodetree.command(help="Show the data of a nodetree.")
@click.argument("index", type=str)
@click.option("--all", is_flag=True, default=False, help="all data of the nodetree.")
def show(index, all):
    from scinode.database.nodetree import NodetreeClient
    import pymongo
    from scinode.database.client import scinodedb

    client = NodetreeClient()
    query = {}
    if "-" in index:
        query["uuid"] = index
    else:
        if index == "last":
            nts = scinodedb["nodetree"].find_one(
                {},
                {"_id": 0, "index": 1},
                sort=[("_id", pymongo.DESCENDING)],
            )
            index = nts["index"]
        query["index"] = int(index)
    client.show(query, all=all)


@nodetree.command(help="Show the log of a nodetree.")
@click.argument("index", type=int)
def log(index):
    from scinode.database.nodetree import NodetreeClient

    client = NodetreeClient()
    query = {}
    query["index"] = index
    client.log(query)


@nodetree.command(help="Delete items of the nodetree.")
@click.option("-n", "--name", help="Name of the item.")
@click.option("-i", "--index", help="Index of the item.", type=int)
@click.option("--uuid", help="uuid of the item.")
@click.option("--state", help="State of the item.")
@click.option("--action", help="Action of the item.")
@click.confirmation_option(prompt="Are you sure you want to delete the items?")
def delete(name, index, uuid, state, action):
    from scinode.database.nodetree import NodetreeClient

    client = NodetreeClient()
    query = {}
    if name:
        query["name"] = {"$regex": name}
    if index:
        query["index"] = index
    if uuid:
        query["uuid"] = uuid
    if state:
        query["state"] = state
    if action:
        query["action"] = action
    client.delete(query)


@nodetree.command(help="Pause nodetrees.")
@click.option("-n", "--name", help="Name of the item.")
@click.option("-i", "--index", help="Index of the item.", type=int)
@click.option("--state", help="State of the item.")
@click.option("--uuid", help="uuid of the item.")
@click.option("--action", help="Action of the item.")
def pause(name, index, uuid, state, action):
    from scinode.database.client import scinodedb
    from scinode.database.nodetree import NodetreeClient

    client = NodetreeClient()
    query = {}
    if name:
        query["name"] = {"$regex": name}
    if index:
        query["index"] = index
    if uuid:
        query["uuid"] = uuid
    if state:
        query["state"] = state
    if action:
        query["action"] = action
    ntdata = scinodedb["nodetree"].find_one(query, {"_id": 0, "uuid": 1})
    nt = DBNodeTree(uuid=ntdata["uuid"])
    nt.pause()


@nodetree.command(help="Play nodetrees.")
@click.option("-n", "--name", help="Name of the item.")
@click.option("-i", "--index", help="Index of the item.", type=int)
@click.option("--state", help="State of the item.")
@click.option("--uuid", help="uuid of the item.")
@click.option("--action", help="Action of the item.")
def play(name, index, uuid, state, action):
    from scinode.database.client import scinodedb
    from scinode.database.nodetree import NodetreeClient

    client = NodetreeClient()
    query = {}
    if name:
        query["name"] = {"$regex": name}
    if index:
        query["index"] = index
    if uuid:
        query["uuid"] = uuid
    if state:
        query["state"] = state
    if action:
        query["action"] = action
    ntdata = scinodedb["nodetree"].find_one(query, {"_id": 0, "uuid": 1})
    nt = DBNodeTree(uuid=ntdata["uuid"])
    nt.play()


@nodetree.command(help="View the nodetree using Blender.")
@click.argument("index", type=int)
def view(index):
    import subprocess

    commands = [
        "blender",
        "--python-exit-code",
        "1",
        "--python-expr",
        "from scinode_editor.api.view import BlenderView; v = BlenderView();v.view({})".format(
            index
        ),
    ]
    proc = subprocess.run(commands)

    if proc.returncode != 0:
        raise RuntimeError("Blender fails with return code {}".format(proc.returncode))


@nodetree.command(help="Export the data of a nodetree.")
@click.argument("index", type=int)
@click.option(
    "--format",
    help="Format of the file.",
    type=click.Choice(["python", "yaml"], case_sensitive=False),
    default="yaml",
)
@click.option("--filename", help="Filename.", type=str)
def export(index, format, filename):
    from scinode.utils.nodetree import nt_export

    query = {"index": index}
    s = nt_export(query, format=format, filename=filename)
    if not filename:
        print(s)


@nodetree.command(help="Import nodetree data from a yaml file.")
@click.argument("filename", type=str)
def launch_from_yaml(filename):
    from scinode import NodeTree

    nt = NodeTree.from_yaml(filename)
    nt.launch()
    print(f"Launch notetree {nt.name} successfully!")


@nodetree.command(help="Edit the data of a nodetree.")
@click.argument("index", type=int)
def edit(index):
    from scinode.database.nodetree import NodetreeClient

    client = NodetreeClient()
    query = {}
    query["index"] = index
    current_nt, data = client.get_yaml_data(query)
    nt_edit = click.edit(current_nt, extension=".toml")
    # print(nt_edit)
    if nt_edit:
        nt = DBNodeTree(uuid=data["uuid"])
        nt.edit_from_yaml(string=nt_edit)
        click.secho(f'Edit nodetree {data["name"]} successfully!', fg="green")
