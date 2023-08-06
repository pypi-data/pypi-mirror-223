import yaml
import os
from pathlib import Path

def collect_tools_from_directory(base_dir) -> dict:
    tools = {}
    for f in Path(base_dir).glob("**/*.yaml"):
        with open(f, "r") as f:
            tools_in_file = yaml.safe_load(f)
            for identifier, tool in tools_in_file.items():
                tools[identifier] = tool
    return tools


def list_package_tools():
    """List package tools"""
    yaml_dir = Path(__file__).parents[1] / "yamls"
    return collect_tools_from_directory(yaml_dir)


class AgentToolConfiguration:
    def __init__(
        self,
        name: str,
        description: str,
        flow_json = None,
    ):
        self.name = name
        self.description = description
        self.flow_json = flow_json