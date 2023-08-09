from promptflow import tool
import os
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
from azure.identity import DefaultAzureCredential
from azureml.core import Workspace
from flow_agent_package.tools.utils import AgentToolConfiguration
SUBSCRIPTION_ENV_NAME = "AZUREML_ARM_SUBSCRIPTION"
RESOURCEGROUP_ENV_NAME = "AZUREML_ARM_RESOURCEGROUP"
WORKSPACE_ENV_NAME = "AZUREML_ARM_WORKSPACE_NAME"

@tool
def get_flow_tool(name: str, description: str, flow_name: str):
  flow_json = get_flow_json(flow_name)
  config = AgentToolConfiguration(name, description, flow_json=flow_json)
  return config

def get_flow_json(flow_name: str) -> str:
    
    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default").token
    sub_id=os.environ[SUBSCRIPTION_ENV_NAME]
    rg=os.environ[RESOURCEGROUP_ENV_NAME]
    ws_name=os.environ[WORKSPACE_ENV_NAME]
    workspace = Workspace(subscription_id=sub_id, resource_group=rg, workspace_name=ws_name)
    endpoint = workspace.service_context._get_endpoint('api')
    url = f"{endpoint}/flow/api/subscriptions/{workspace.subscription_id}/resourcegroups/" + \
          f"{workspace.resource_group}/providers/Microsoft.MachineLearningServices/workspaces/" + \
          f"{workspace.name}/Flows/"
    print(f"URL: {url}")
    headers = {
        'Authorization': f'Bearer {token}',
        'content-type': 'application/json'
    }
    import requests
    flows = requests.get(url, headers=headers).json()
    print(f"flows: {flows}")
    correct_flow = None
    for flow in flows:
        if flow["flowName"] == flow_name:
            correct_flow = flow
            break
    print(correct_flow)
    specific_url = url + correct_flow["flowId"] + "?experimentId=" + correct_flow["experimentId"]
    flow_json = requests.get(specific_url, headers=headers).json()
    print(flow_json)
    print(flow_json.keys())
    graph = flow_json["flow"]["flowGraph"]
    batch_inputs = flow_json["flowRunSettings"]["batch_inputs"]
    connections = []
    for node in graph["nodes"]:
        if node.get("connection"):
            connections.append(node.get("connection"))
        if node.get("inputs", {}).get("connection"):
            connections.append(node["inputs"]["connection"])
    connection_configs = {}
    for connection_name in set(connections):
        url = f"{endpoint}/rp/workspaces/subscriptions/{workspace.subscription_id}/resourcegroups/" + \
          f"{workspace.resource_group}/providers/Microsoft.MachineLearningServices/workspaces/" + \
          f"{workspace.name}/connections/{connection_name}/listsecrets?api-version=2023-02-01-preview"

        connection_json = requests.post(url, headers=headers).json()
        config = {
            "type": "AzureOpenAIConnection",
            "value": {
                "api_key": connection_json["properties"]["credentials"]["key"],
                "api_base": connection_json["properties"]["target"],
                "api_type": "azure",
                "api_version": "2023-03-15-preview"
            }
        }
        connection_configs[connection_name] = config
    
    final_json = {
        "flowName": correct_flow["flowName"],
        "description": correct_flow["description"],
        "flowId": correct_flow["flowId"],
        "flow": graph,
        "batch_inputs": batch_inputs,
        "connections": connection_configs
    }
    return final_json
