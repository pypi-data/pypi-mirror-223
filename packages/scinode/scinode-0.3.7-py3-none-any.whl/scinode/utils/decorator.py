from typing import Any


def inspect_function(func: Any):
    """inspect the arguments of a function, and return a list of arguments
    and a list of keyword arguments, and a list of default values
    and a list of annotations

    Args:
        func (Any): any function

    Returns:
        tuple: (args, kwargs, defaults, annotations)
    """
    import inspect

    # Get the signature of the function
    signature = inspect.signature(func)

    # Get the parameters of the function
    parameters = signature.parameters

    # Iterate over the parameters
    args = []
    kwargs = {}
    var_args = None
    var_kwargs = None
    for name, parameter in parameters.items():
        if parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
            if parameter.annotation is not inspect.Parameter.empty:
                arg = [name, parameter.annotation]
            else:
                arg = [name, None]
            args.append(arg)
        elif parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            kwargs[name] = {"type": parameter.annotation}
            if parameter.default is not inspect.Parameter.empty:
                kwargs[name]["default"] = parameter.default
            else:
                kwargs[name]["default"] = None
        elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            var_args = name
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            var_kwargs = name
                
    return args, kwargs, var_args, var_kwargs


def python_type_to_socket_type(python_type):
    """Convert python type to socket type"""
    if python_type == int:
        return "Int"
    elif python_type == float:
        return "Float"
    elif python_type == str:
        return "String"
    elif python_type == bool:
        return "Bool"
    else:
        return "General"


def generate_input_sockets(func: Any, inputs=None, properties=None):
    """Generate input sockets from a function.
    If the input sockets is not given, then the function
    will be used to update the input sockets."""
    inputs = inputs or []
    properties = properties or []
    args, kwargs, var_args, var_kwargs = inspect_function(func)
    names = [input[1] for input in inputs] + [property[1] for property in properties]
    for arg in args:
        if arg[0] not in names:
            inputs.append([python_type_to_socket_type(arg[1]), arg[0]])
    for name, kwarg in kwargs.items():
        if name not in names:
            input = [python_type_to_socket_type(kwarg["type"]), name]
            if kwarg["default"] is not None:
                # prop: [identifier, kwargs]
                input.append({"property": [input[0], {"default": kwarg["default"]}]})
            inputs.append(input)
    if var_args is not None:
        inputs.append(["General", var_args])
    if var_kwargs is not None:
        inputs.append(["General", var_kwargs])
    #
    arg_names = [arg[0] for arg in args]
    kwarg_names = [name for name in kwargs.keys()]
    return arg_names, kwarg_names, var_args, var_kwargs, inputs


def create_node(ndata):
    """Create a node class from node data.

    Args:
        ndata (dict): node data

    Returns:
        _type_: _description_
    """
    from scinode.core.node import Node

    class MyNode(Node):
        identifier: str = ndata["identifier"]
        node_type: str = ndata["node_type"]
        catalog = ndata.get("catalog", "Others")
        register_path = ndata.get("register_path", "")

        def create_properties(self):
            for prop in ndata.get("properties", []):
                kwargs = prop[2] if len(prop) > 2 else {}
                self.properties.new(prop[0], prop[1], **kwargs)

        def create_sockets(self):
            for input in ndata.get("inputs", []):
                inp = self.inputs.new(input[0], input[1])
                setting = input[2] if len(input) > 2 else {}
                # print("input: ", input, "setting: ", setting)
                prop = setting.get("property", None)
                if prop is not None:
                    kwargs = prop[1] if len(prop) > 1 else {}
                    # identifer, name, kwargs
                    inp.add_property(prop[0], input[1], **kwargs)
                inp.link_limit = setting.get("link_limit", 1)
            for output in ndata.get("outputs", []):
                self.outputs.new(output[0], output[1])
            self.args = ndata.get("args", [])
            self.kwargs = ndata.get("kwargs", [])
            self.var_args = ndata.get("var_args", None)
            self.var_kwargs = ndata.get("var_kwargs", None)

        def get_executor(self):
            executor = ndata.get("executor", {})
            return executor

    return MyNode


def create_node_group(ngdata):
    """Create a node group class from node group data.

    Args:
        ngdata (dict): node data

    Returns:
        _type_: _description_
    """
    from scinode.core.node import Node

    class MyNodeGroup(Node):
        identifier: str = ngdata["identifier"]
        node_type: str = "GROUP"
        catalog = ngdata.get("catalog", "Others")
        register_path = ngdata.get("register_path", "")

        def get_default_node_group(self):
            nt = ngdata["nt"]
            nt.name = self.name
            nt.uuid = self.uuid
            nt.parent_node = self.uuid
            nt.worker_name = self.worker_name
            return ngdata["nt"]

    return MyNodeGroup


def register_node(
    identifier,
    node_type="Normal",
    args={},
    kwargs={},
    properties=[],
    inputs=[],
    outputs=[],
    executor={},
    register_path="",
    catalog="Others",
):
    from scinode.utils import register
    from scinode.nodes import node_pool

    ndata = {
        "identifier": identifier,
        "node_type": node_type,
        "catalog": catalog,
        "args": args,
        "kwargs": kwargs,
        "properties": properties,
        "inputs": inputs,
        "outputs": outputs,
        "executor": executor,
        "register_path": register_path,
    }
    node = create_node(ndata)
    try:
        register(node_pool, [node])
    except Exception as e:
        return None
    return node


def register_node_group(identifier, nt, register_path="", catalog="Others"):
    from scinode.utils import register
    from scinode.nodes import node_pool

    ngata = {
        "identifier": identifier,
        "catalog": catalog,
        "nt": nt,
        "register_path": register_path,
    }
    node = create_node_group(ngata)
    try:
        register(node_pool, [node])
    except Exception as e:
        return None
    return node


# decorator with arguments indentifier, args, kwargs, properties, inputs, outputs, executor
def decorator_node(
    identifier=None,
    node_type="Normal",
    properties=None,
    inputs=None,
    outputs=None,
    catalog="Others",
    executor_type="function",
):
    """Generate a decorator that register a function as a SciNode node.

    Attributes:
        indentifier (str): node identifier
        catalog (str): node catalog
        args (list): node args
        kwargs (dict): node kwargs
        properties (list): node properties
        inputs (list): node inputs
        outputs (list): node outputs
    """
    properties = properties or []
    inputs = inputs or []
    outputs = outputs or []

    def decorator(func):
        import cloudpickle as pickle

        nonlocal identifier

        if identifier is None:
            identifier = func.__name__

        # use cloudpickle to serialize function
        executor = {
            "executor": pickle.dumps(func),
            "type": executor_type,
            "is_pickle": True,
        }
        #
        # Get the args and kwargs of the function
        args, kwargs, var_args, var_kwargs, _inputs = generate_input_sockets(func, inputs, properties)
        ndata = {
            "identifier": identifier,
            "node_type": node_type,
            "args": args,
            "kwargs": kwargs,
            "var_args": var_args,
            "var_kwargs": var_kwargs,
            "properties": properties,
            "inputs": _inputs,
            "outputs": outputs,
            "executor": executor,
            "catalog": catalog,
        }
        node = create_node(ndata)
        func.identifier = identifier
        func.node = node
        return func

    return decorator


# decorator with arguments indentifier, args, kwargs, properties, inputs, outputs, executor
def decorator_node_group(identifier, catalog="Others", executor_path=None):
    """Generate a decorator that register a function as a SciNode node.

    Attributes:
        indentifier (str): node identifier
    """

    def decorator(func):
        import cloudpickle as pickle

        # use cloudpickle to serialize function
        executor = {
            "executor": pickle.dumps(func),
            "type": "pickle",
        }
        nt = func()
        node = register_node_group(identifier, nt, catalog=catalog)
        return node

    return decorator


class NodeDecoratorCollection:
    """Collection of node decorators."""

    node = staticmethod(decorator_node)
    group = staticmethod(decorator_node_group)

    __call__: Any = node  # Alias '@node' to '@node.node'.


node = NodeDecoratorCollection()

if __name__ == "__main__":

    @node.group("TestAdd")
    def my_add_group():
        from scinode import NodeTree

        nt = NodeTree()
        add1 = nt.nodes.new("TestAdd", "add1")
        add2 = nt.nodes.new("TestAdd", "add2")
        add3 = nt.nodes.new("TestAdd", "add3")
        nt.links.new(add1.outputs[0], add3.inputs[0])
        nt.links.new(add2.outputs[0], add3.inputs[1])
        nt.group_properties = [
            ("add1", "t", "t1"),
            ("add2", "t", "t2"),
        ]
        nt.group_inputs = [("add1", "x", "x"), ("add2", "x", "y")]
        nt.group_outputs = [("add3", "Result", "Result")]
        return nt
