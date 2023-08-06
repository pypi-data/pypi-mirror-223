import csv
import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp
from typing import Dict, List, Union

from promptflow.contracts.run_mode import RunMode
from promptflow.runtime.contracts.runtime import SubmitFlowRequest
from flow_agent_package.tools.utils import AgentToolConfiguration

from promptflow import ToolProvider, tool
from promptflow.core.tools_manager import register_builtin_method, register_apis
from promptflow.runtime import PromptFlowRuntime
from promptflow.core.thread_local_singleton import ThreadLocalSingleton
from langchain.agents import Tool
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import AzureChatOpenAI
import os
import urllib.request
import urllib.error
import json
import ssl
import openai
from promptflow.connections import (
    AzureOpenAIConnection,
    SerpConnection,
    CustomConnection,
)
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import BaseLanguageModel

def convert_request_to_raw(
    request,
    query,
    source_run_id=None,
    run_mode: RunMode = RunMode.Flow,
) -> dict:
    """Refine the request to raw request dict"""
    flow_run_id = str(uuid.uuid4())
    if not source_run_id:
        source_run_id = str(uuid.uuid4())
    variant_runs = request.get("variants_runs", {})
    if variant_runs:
        request["variants_runs"] = {v: f"{vid}_{flow_run_id}" for v, vid in variant_runs.items()}
    if request.get("eval_flow_run_id"):
        request["eval_flow_run_id"] = f"{request['eval_flow_run_id']}_{flow_run_id}"
    if "id" not in request["flow"]:
        request["flow"]["id"] = str(uuid.uuid4())
    inputs = request["batch_inputs"]
    for key in inputs[0]:
        inputs[0][key] = query
    request["batch_inputs"] = inputs
    print(f"inputs: {inputs}")
    return {
        "FlowId": request["flow"]["id"],
        "FlowRunId": flow_run_id,
        "SourceFlowRunId": source_run_id,
        "SubmissionData": json.dumps(request),
        "RunMode": run_mode,
        "BatchDataInput": request.get("batch_data_input", {}),
    }

def custom_active_instance(self, force=False):
    # def _activate_in_context(self, force=False):
    instance = self.active_instance()
    if instance is not None and instance is not self and not force:
        return
        #raise NotImplementedError(f"Cannot set active dummy since there is another active instance: {instance}")
    self.context_var.set(self)


class FlowTool():


    def __init__(self, config: AgentToolConfiguration):
        self.name = config.name
        self.description = config.description
        self.flow_json = config.flow_json

    def get_run_func(self):
        
        def run_str(query):
            result = self.execute(query)
            return json.dumps(result)
        
        return run_str

    def execute(self, query) -> dict:
        #batch_request = json.loads(input_json)
        input_json = self.flow_json
        run_mode = RunMode.Flow
        raw_request = convert_request_to_raw(input_json, query, None, run_mode)
        flow_request = SubmitFlowRequest.deserialize(raw_request)

        ThreadLocalSingleton._activate_in_context = custom_active_instance

        runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
        start = datetime.now()
        old_setting = runtime.config.execution.execute_in_process
        runtime.config.execution.execute_in_process = False
        
        result = runtime.execute(flow_request)
        runtime.config.execution.execute_in_process = old_setting
        end = datetime.now()
        return result
@tool
def pick_tool_and_execute(
    query: str,
    llm_connection: AzureOpenAIConnection,
    config1: AgentToolConfiguration,
    config2: AgentToolConfiguration,
    config3: AgentToolConfiguration
):
    print(query)
    print(f"config1: {config1}")

    tool_configs = [config1, config2, config3]
    tools = []
    for config in tool_configs:
        tool = FlowTool(config)
        run_func = tool.get_run_func()
        from langchain.agents import Tool
        lang_tool = Tool(
                name=tool.name,
                func=run_func,
                description=tool.description,
                return_direct=True
            )
        tools.append(lang_tool)
    
        
    openai.api_base = llm_connection.api_base
    openai.api_type = llm_connection.api_type
    openai.api_version = llm_connection.api_version
    # todo: parameterize model_name and temperature
    llm = AzureChatOpenAI(client=openai.ChatCompletion,
                            temperature=0, 
                            deployment_name="gpt-35-turbo",
                            model_name="gpt-35-turbo", 
                            openai_api_key=llm_connection.api_key,
                            openai_api_base=llm_connection.api_base,
                            openai_api_type=llm_connection.api_type,
                            openai_api_version=llm_connection.api_version)
    agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION
    agent = initialize_agent(
            tools,
            llm,
            agent=agent_type,
            verbose=True)
    answer = agent.run(query)
    # answer = execute(query, config1.name, config1.flow_json)
    return answer

    
def execute(query, name, input_json, run_mode=RunMode.Flow, raise_ex=True) -> dict:
    #batch_request = json.loads(input_json)
    raw_request = convert_request_to_raw(input_json, query, None, run_mode)
    flow_request = SubmitFlowRequest.deserialize(raw_request)

    ThreadLocalSingleton._activate_in_context = custom_active_instance

    runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
    start = datetime.now()
    old_setting = runtime.config.execution.execute_in_process
    runtime.config.execution.execute_in_process = False
    
    result = runtime.execute(flow_request)
    runtime.config.execution.execute_in_process = old_setting
    end = datetime.now()
    if name == 'Dummy':
        answer = result["flow_runs"][0]["output"]["answer"][0]
    else:
        answer = result
    return answer


# register_builtin_method(execute)