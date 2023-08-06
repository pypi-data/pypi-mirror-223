import re
from Katana import NodegraphAPI, AssetAPI
from ciopath.gpath_list import PathList
from ciopath.gpath import Path


# we only need the regex to find udims, since file sequences are handled by methods of the FileSequencePlugin.
# Any words contained in angle should do the trick.
DEFAULT_UDIM_REGEX = r"<\w+>"

DEFAULT_NODE_BLACKLIST = (
    "Group",
    "ErrorNode",
    "RootNode",
    "Render",
    "ConductorRender",
    "AttributeScript::user.outputPath",
    "AttributeScript::user.outputStats",
    "AttributeScript::user.scenePath",
)

DEFAULT_PATH_PREFIX_BLACKLIST = ("/tmp/", "/var/tmp/", "/usr/tmp/", "/root", "//*","{", "[")

VALID_FILENAME_REGEX = re.compile(r'^[^?%*:|"<>]+\.[^?%*:|"<>]+$')


def _stringy(param):
    """Check if the parameter is a string type.

    Args:
        param (NodegraphAPI.Parameter): The parameter to check.

    Returns:
        bool: True if the parameter is a string type and not a cel, False otherwise.
    """
    if not param.getType() == "string":
        return False

    try:
        hint = eval(param.getHintString())
        if hint.get("widget") in ["cel", "scenegraphLocation"]:
            return False
    except:
        pass
    return True

def _flatten_param(param, result):
    """Recursively flatten the parameter into a list.

    Args:
        param (NodegraphAPI.Parameter): The parameter to flatten.
        result (list): The list to append the flattened parameters to.
    """
    if param.getType() == "string":
        result.append(param)
    elif param.getType() in ("group", "stringArray"):
        for child in param.getChildren():
            _flatten_param(child, result)


def _find_expression_source(param):
    """Find the source of an expression.

    If the parameter is not a reference expression, the parameter itself is
    returned.

    Args:
        param (NodegraphAPI.Parameter): The parameter with an expression.

    Returns:
        NodegraphAPI.Parameter: The source parameter of the expression.
    """
    if param.isExpression():
        expr = param.getExpression().strip()
        if re.compile(r"^getParam\([ \'\"0-9a-zA-Z_\.]+\)$").findall(expr):
            node_param = re.compile(r"\([ \'\"0-9a-zA-Z_\.]+\)$").findall(expr)[0]
            node_param = re.compile(r"[a-zA-Z0-9_.]+").findall(node_param)[0]
            node_name = node_param.split(".")[0]
            node = NodegraphAPI.GetNode(node_name)
            if node:
                param_name = ".".join(node_param.split(".")[1:])
                new_param = node.getParameter(param_name)
                if new_param:
                    return _find_expression_source(new_param)

        elif re.compile(r"^getParent\(\)\.[0-9a-zA-Z_\.]+$").findall(expr):
            node = param.getNode().getParent()
            if node:
                param_name = re.compile(r"\.[0-9a-zA-Z_\.]+$").findall(expr)[0]
                new_param = node.getParameter(param_name.strip("."))
                if new_param:
                    return _find_expression_source(new_param)

    return param


def _get_gpath(filename):
    """Get the path asset from the parameter.

    If the asset is not an absolute path, None is returned. NOTE, that this means we ignore, for example, textures that are expected to be found in Rendermnan's search paths. We assume the relevant assets and paths exist on the cloud instance.

    The asset might not exist on disk. For example: /tmp/asset.*.abc will be globbed later.

    Args:
        param (NodegraphAPI.Parameter): The parameter to get the gpath from.

    Returns:
        ciopath.gpath.Path: The gpath object.
    """
    try:
        asset = Path(filename)
    except ValueError:
        return None

    if not asset.absolute:
        return None

    return asset


class AssetScraper(object):
    """Class to scrape assets used in the project."""

    def __init__(
        self,
        regex=DEFAULT_UDIM_REGEX,
        node_blacklist=DEFAULT_NODE_BLACKLIST,
        path_prefix_blacklist=DEFAULT_PATH_PREFIX_BLACKLIST,
        file_sequence_plugin=AssetAPI.GetDefaultFileSequencePlugin(),
    ):
        """Initialize the AssetScraper class."""
        self.asset_pairs = []
        self.node_blacklist = tuple(node_blacklist)
        self.path_prefix_blacklist = tuple(path_prefix_blacklist)
        self.regex = re.compile(regex, re.IGNORECASE)
        self.file_sequence_plugin = file_sequence_plugin

        self.seen_params = set()

    def scrape(self):
        """Scan the nodegraph for assets.

        Returns:
            ciopath.gpath_list.PathList: The list of assets found.
        """
        nodes = NodegraphAPI.GetAllNodes(includeDeleted=False)

        for node in nodes:
            
            # fill flat_parameters.
            flat_parameters = []
            _flatten_param(node.getParameters(), flat_parameters)

            for param in flat_parameters:
                if param in self.seen_params:
                    continue
                self.seen_params.add(param)

                if not _stringy(param):
                    continue

                param = _find_expression_source(param)

                if self._is_blacklisted(node, param):
                    continue
                filename = param.getValue(0)
                filename = self._make_globbable(filename)
                path_obj = _get_gpath(filename)
                if path_obj:
                    self.asset_pairs.append((param, path_obj))


    def get_path_list(self):
        """
        Returns a PathList object containing all the assets in self.asset_pairs.

        Args:
            None

        Returns:
            PathList: A PathList object containing all the assets.

        """
        path_list = PathList()
        for _, asset in self.asset_pairs:
            path_list.add(asset)
        return path_list

    def _is_blacklisted(self, node, param):
        """Check if the node and parameter are blacklisted.

        Args:
            node (NodegraphAPI.Node): The node to check.
            param (NodegraphAPI.Parameter): The parameter to check.

        Returns:
            bool: True if the node and parameter are blacklisted, False otherwise.
        """
        node_type = param.getNode().getType()
        if node.getParameter("user.macroType"):
            node_type = node.getParameter("user.macroType").getValue(0)

        if node_type in self.node_blacklist:
            return True

        param_name = param.getFullName(False)
        if f"{node_type}::{param_name}" in self.node_blacklist:
            return True

        filename = param.getValue(0)
        if filename.startswith(self.path_prefix_blacklist):
            return True
        return False

    def _make_globbable(self, filename):
        """Replace all sequence ranges and regex matches with a globbable pattern.

        Args:
            filename (str): The filename to be made globbable.

        Returns:
            str: The globbable version of the filename.
        """
        if self.file_sequence_plugin.isFileSequence(filename):
            file_sequence = self.file_sequence_plugin.getFileSequence(filename)
            filename = file_sequence.getPrefix() + "*" + file_sequence.getSuffix()
        filename = self.regex.sub(r"*", filename)
        return filename
