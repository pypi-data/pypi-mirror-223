from scinode.orm import DBItem
from scinode.common.log import logging

logger = logging.getLogger("orm")


class DBNode(DBItem):
    """DBNode Class.
    Object Relational Mapping for Node.

    db_name: str
        name of the database.
    uuid: str
        uuid of the node.
    name: str
        name of the node.

    Example:

    >>> # load node from database
    >>> node = DBNode(uuid=uuid)
    """

    db_name: str = "node"

    def __init__(self, uuid=None, dbdata=None) -> None:
        """init a instance

        Args:
            uuid (str, optional): uuid of the node.
                Defaults to None.
            dbdata (dict, optional): data of the node from database.
                Defaults to None.
        """
        if dbdata:
            uuid = dbdata["uuid"]
        super().__init__(uuid)
        self.record = self.dbdata
        self.name = self.record["name"]
        self.inner_id = self.record["inner_id"]
        self.scattered_from = self.record["metadata"]["scattered_from"]
        self.scattered_label = self.record["metadata"]["scattered_label"]

    def copy(
        self,
        name=None,
        nodetree_uuid=None,
        is_scattered_node=False,
        scattered_label="",
        is_ref=False,
    ):
        """Copy this node to a new item and insert it into the database.

        Args:
            name (str): name of the new node
            nodetree_uuid (str): uuid of the nodetree.
            is_scattered_node (bool, optional): Is it a scattered node.
                Defaults to False.

        Returns:
            DBNode: a node
        """
        import uuid
        from scinode.utils.node import get_node_data

        record = get_node_data({"uuid": self.uuid}, {"_id": 0})
        # change name and uuid
        if name:
            record["name"] = name
        record["state"] = "CREATED"
        record["action"] = "NONE"
        record["uuid"] = str(uuid.uuid1())
        # print(record)
        # update uuid in link, now we can only update half
        inputs = record["inputs"]
        for input in inputs:
            for link in input["links"]:
                link["to_node"] = record["name"]
        record["inputs"] = inputs
        outputs = record["outputs"]
        for output in outputs:
            # for ref node, the sockek uuid should not be updated.
            if not is_ref:
                output["uuid"] = str(uuid.uuid1())
            for link in output["links"]:
                link["from_node"] = record["name"]
        record["outputs"] = outputs
        if nodetree_uuid is not None:
            record["metadata"]["nodetree_uuid"] = nodetree_uuid
        if is_scattered_node:
            record["metadata"]["scattered_from"] = self.uuid
            record["metadata"]["scattered_label"] = scattered_label
        # self.insert_one(record)
        # node = self.__class__(uuid=record["uuid"])
        if is_ref:
            record["metadata"]["node_type"] = "REF"
            record["metadata"]["ref_uuid"] = self.uuid
            record["state"] = "FINISHED"
            record["action"] = "NONE"
        return record

    @classmethod
    def update_from_dict(cls, data):
        """Udpate node from dict data.
        Set metadata and properties.
        """
        from scinode.utils.node import get_node_data

        ndata = get_node_data({"uuid": data["uuid"]})
        for key in ["uuid", "state", "action", "description", "hash"]:
            if data.get(key):
                ndata[key] = data.get(key)
        for key in ["worker_name"]:
            if data.get(key):
                ndata["metadata"][key] = data.get(key)
        # properties
        for name, p in data["properties"].items():
            ndata["properties"][name]["value"] = p
        new_inputs = data.get("inputs", None)
        if new_inputs:
            # links
            index = {}
            for i, input in enumerate(ndata["inputs"]):
                index[input["name"]] = i
                input["links"] = []
            # print(new_inputs)
            for link in new_inputs:
                # print("link: ", link)
                link["to_node"] = ndata["name"]
                ndata["inputs"][index[link["to_socket"]]]["links"].append(link)
        return ndata

    def update_from_yaml(self, filename=None, string=None):
        """update node from yaml file.

        Args:
            filename (str, optional): _description_. Defaults to None.
            string (str, optional): _description_. Defaults to None.

        Returns:
            node: _description_
        """
        from scinode.utils import load_yaml

        # load data
        ndata = load_yaml(filename=filename, string=string)
        self.update_from_dict(ndata)

    @property
    def dbdata(self):
        """Item data from database

        Returns:
            dict: _description_
        """
        from scinode.utils.node import get_node_data

        query = {"uuid": self.uuid}
        dbdata = get_node_data(query)
        return dbdata

    @property
    def nodetree_uuid(self):
        dbdata = self.get_dbdata({"uuid": self.uuid}, {"metadata.nodetree_uuid": 1})
        return dbdata["metadata"]["nodetree_uuid"]

    def reset(self, launch=False):
        """Reset node. Include all its properties:
        states, counter and results.
        """
        if self.record["metadata"]["node_type"] in ["REF"]:
            return

        if launch:
            action = "LAUNCH"
        else:
            action = "NONE"
        counter = 0
        self.update_db_keys(
            {
                "state": "CREATED",
                "action": action,
                "counter": counter,
            }
        )

    def getstate(self):
        from scinode.database.db import scinodedb

        query = {"uuid": self.nodetree_uuid}
        data = scinodedb["nodetree"].find_one(query, {"_id": 0, "nodes": 1})["nodes"]
        return data[self.name].get("state")

    def getaction(self):
        from scinode.database.db import scinodedb

        query = {"uuid": self.nodetree_uuid}
        data = scinodedb["nodetree"].find_one(query, {"_id": 0, "nodes": 1})["nodes"]
        return data[self.name].get("action")

    def get_result(self, uuid):
        """Get result by the output uuid."""
        from scinode.database.client import scinodedb
        from scinode.utils.node import deserialize_item

        query = {"uuid": uuid}
        data = scinodedb["data"].find_one(query, {"_id": 0})
        if data:
            return deserialize_item(data)

    @property
    def properties(self):
        return self.get_properties()

    def get_properties(self):
        from scinode.utils.node import get_node_data
        from scinode.orm.db_property import DBProperty

        query = {"uuid": self.uuid}
        proj = {"_id": 0, "properties": 1}
        ndata = get_node_data(query, proj=proj)
        properties = []
        for name, data in ndata["properties"].items():
            prop = DBProperty(node_uuid=self.uuid, name=name)  # , self.worker_name)
            properties.append(prop)
        return properties

    @property
    def inputs(self):
        return self.get_inputs()

    def get_inputs(self):
        from scinode.utils.node import get_node_data
        from scinode.orm.db_socket import DBSocket

        query = {"uuid": self.uuid}
        proj = {"_id": 0, "inputs": 1}
        ndata = get_node_data(query, proj=proj)
        inputs = []
        for data in ndata["inputs"]:
            socket = DBSocket(type="input", dbdata=data)  # , self.worker_name)
            inputs.append(socket)
        return inputs

    @property
    def outputs(self):
        return self.get_outputs()

    def get_outputs(self):
        from scinode.utils.node import get_node_data
        from scinode.orm.db_socket import DBSocket

        query = {"uuid": self.uuid}
        proj = {"_id": 0, "outputs": 1}
        ndata = get_node_data(query, proj=proj)
        outputs = []
        for data in ndata["outputs"]:
            socket = DBSocket(type="output", dbdata=data)  # , self.worker_name)
            outputs.append(socket)
        return outputs

    @property
    def results(self):
        return self.get_results()

    def get_results(self):
        """Get all results."""
        from scinode.utils.node import get_results

        results = get_results(self.uuid)
        return results

    def __repr__(self) -> str:
        s = ""
        s += 'Node(name="{}", uuid="{}", inputs = ['.format(self.name, self.uuid)
        for input in self.inputs:
            s += '"{}", '.format(input.name)
        s += "], outputs = ["
        for output in self.outputs:
            s += '"{}", '.format(output.name)
        s += "])\n"
        return s
