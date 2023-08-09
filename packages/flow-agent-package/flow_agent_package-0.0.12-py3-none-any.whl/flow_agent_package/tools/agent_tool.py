import csv
import json
from enum import Enum
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
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    OpenAITextCompletion,
    AzureTextCompletion,
    AzureChatCompletion
)
import json
from semantic_kernel import Kernel
from semantic_kernel.skill_definition import (
    sk_function,
)
from semantic_kernel.orchestration.sk_context import SKContext


class AribitrationMethod(Enum):
  LANGCHAIN = "Langchain"
  OPENAI_FUNCTIONS = "OpenAI Functions"
  SEMANTIC_KERNEL = "Semantic Kernel"


def convert_request_to_raw(
    request,
    inputs,
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
    if isinstance(inputs, str):
      old_inputs = request["batch_inputs"]
      for key in old_inputs[0]:
          old_inputs[0][key] = inputs
      request["batch_inputs"] = old_inputs
    elif isinstance(inputs, dict):
      request["batch_inputs"] = [inputs]

    print(f"final inputs: {request['batch_inputs']}")
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

class OrchestratorPlugin:
    def __init__(self, kernel: Kernel):
        self._kernel = kernel

    @sk_function(
        description="Routes the request to the appropriate function",
        name="route_request",
    )
    async def RouteRequest(self, context: SKContext) -> str:
        # Save the original user request
        request = context["input"]

        native_funcs = self._kernel.skills.get_functions_view().native_functions["FlowPlugin"]
        func_options = [function.name for function in native_funcs]
        print(f"Functions returnedL {func_options}")
        # Add the list of available functions to the context
        context["options"] = " ,".join(func_options)
         
        # Retrieve the intent from the user request
        GetIntent = self._kernel.skills.get_function("OrchestratorPlugin", "GetIntent")
        FormatResponse = self._kernel.skills.get_function(
            "OrchestratorPlugin", "FormatResponse"
        )
        await GetIntent.invoke_async(context=context)
        intent = context["input"].strip()
        
        print(f"context: {intent}")
 
        # Prepare the functions to be called in the pipeline
        # GetNumbers = self._kernel.skills.get_function(
        #     "OrchestratorPlugin", "GetNumbers"
        # )
        # ExtractNumbersFromJson = self._kernel.skills.get_function(
        #     "OrchestratorPlugin", "extract_numbers_from_json"
        # )

        # Retrieve the correct function based on the intent
        
        picked_function = self._kernel.skills.get_function("FlowPlugin", intent)
        

        # Create a new context object with the original request
        pipelineContext = self._kernel.create_new_context()
        pipelineContext["original_request"] = request
        pipelineContext["input"] = request

        # Run the functions in a pipeline
        output = await self._kernel.run_async(
            picked_function,
            FormatResponse,
            input_context=pipelineContext,
        )
        print(f"Final output: {output}")
        return output["input"]


intent_prompt = """
User: {{$input}}

---------------------------------------------

Provide the intent of the user. The intent should be one of the following: {{$options}}

INTENT: 
"""

format_response = """
The answer to the users request is: {{$input}}
The bot should provide the answer back to the user.

User: {{$original_request}}
Bot: 
"""


class FlowFunction():

    def __init__(self, config: AgentToolConfiguration):
        self.name = config.name
        self.tool_description = config.description
        self.function_description = self.init_description(config)
        self.input_config = self.init_inputs(config.flow_json)
        self.output_list = self.init_outputs(config.flow_json)
        self.flow_json = config.flow_json

    def init_inputs(self, flow_json):
      base_inputs = flow_json["flow"]["inputs"]
      input_config = {}
      for input_name, input_info in base_inputs.items():
        input_type = input_info.get("type")
        if input_type == None:
          raise Exception(f"Input {input_name} for tool {self.name} does not have a type specified!")
        # elif input_type == "object"
        #   raise Exception(f"Input {input_name} for tool {self.name} has incompatible type: {input_type}")
        
        input_description = input_info.get("description")
        # if input_description == None:
        #   raise Exception(f"Input {input_name} for tool {self.name} does not have a description!")
        temp = {"type": input_type}
        if input_description:
          temp["description"] = input_description
        input_config[input_name] = temp
      return input_config
    
    def init_outputs(self, flow_json):
      outputs = flow_json["flow"]["outputs"]
      return outputs.keys()
    
    def init_description(self, config):
      config_desc = config.description
      return config.flow_json.get("description", config_desc)

    def to_function_definition(self):
      return {
        "name": self.flow_json["flowName"].replace(" ", "_"),
        "description": self.function_description,
        "parameters":{
          "type": "object",
          "properties": self.input_config
        }
      }

    def to_run_function(self):
        
        def run_str(query):
            result = self.execute(query)
            return json.dumps(result)
        
        return run_str

    def to_sk_function(self):
      @sk_function(
          description=self.function_description,
          name=self.name
      )
      def sk_execute_func(query: str) -> str:
        result = self.execute(query)
        return json.dumps(result)
        # parse inputs from query using another tool?
      return sk_execute_func
        # Execute
    
    def execute(self, inputs) -> dict:
        raw_request = convert_request_to_raw(self.flow_json, inputs, None, RunMode.Flow)
        flow_request = SubmitFlowRequest.deserialize(raw_request)

        ThreadLocalSingleton._activate_in_context = custom_active_instance

        runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
        start = datetime.now()
        old_setting = runtime.config.execution.execute_in_process
        runtime.config.execution.execute_in_process = False
        
        result = runtime.execute(flow_request)
        runtime.config.execution.execute_in_process = old_setting
        end = datetime.now()
        result = result["flow_runs"][0]["output"]
        return result

@tool
def pick_tool_and_execute(
    query: str,
    arbitration_method: AribitrationMethod,
    llm_connection: AzureOpenAIConnection,
    config1: AgentToolConfiguration,
    config2: AgentToolConfiguration,
    config3: AgentToolConfiguration
):
  print(f"arbitration method: {arbitration_method}")  
  flow_tools = [FlowFunction(config1), FlowFunction(config2)] #, FlowFunction(config3)]
  openai.api_base = llm_connection.api_base
  openai.api_type = llm_connection.api_type
  openai.api_version = "2023-07-01-preview"
  openai.api_key = llm_connection.api_key

  if arbitration_method == AribitrationMethod.LANGCHAIN.value:
    print("Using Langchain")
    tools = []
    for tool in flow_tools:
        run_func = tool.to_run_function()
        from langchain.agents import Tool
        lang_tool = Tool(
                name=tool.name,
                func=run_func,
                description=tool.tool_description,
                return_direct=True
            )
        tools.append(lang_tool)
    
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
  elif arbitration_method == AribitrationMethod.OPENAI_FUNCTIONS.value:
    # Call OpenAI to pick function
    print("Using Functions")
    functions = []
    function_names_mapping = {}
    for tool in flow_tools:
      func_def = tool.to_function_definition()
      functions.append(func_def)
      function_names_mapping[func_def["name"]] = tool

    messages = [
      {
        "role": "system",
        "content": "Assistant is a helpful assistant that is good at using provided functions to get answers to specific questions. You must pick a function as a response"
      },
      {
        "role": "user",
        "content": query
      }
    ]
    print(f"Functions: {functions}")
    response = openai.ChatCompletion.create(
        deployment_id="gpt-35-turbo",
        messages=messages,
        functions=functions,
        function_call="auto", 
    )
    response_message = response["choices"][0]["message"]
    print(f"Response from OpenAI: {response_message}")
    # Call Function
    if response_message.get("function_call"):
        print("Recommended Function call:")
        print(response_message.get("function_call"))
        print()
        
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        
        function_name = response_message["function_call"]["name"]
        
        # verify function exists
        if function_name not in function_names_mapping:
            return "Function " + function_name + " does not exist"
        tool_to_use = function_names_mapping[function_name]  
        
        # verify function has correct number of arguments
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(f"Function Args: {function_args}")
        # if check_args(function_to_call, function_args) is False:
        #     return "Invalid number of arguments for function: " + function_name
        flow_result = tool_to_use.execute(function_args)

        print("Output of function call:")
        print(flow_result)
        print()

        messages.append(
            {
                "role": response_message["role"],
                "name": response_message["function_call"]["name"],
                "content": response_message["function_call"]["arguments"],
            }
        )

        # adding function response to messages
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": json.dumps(flow_result),
            }
        )  # extend conversation with function response

        print("Messages in next request:")
        for message in messages:
            print(message)
        print()

        response = openai.ChatCompletion.create(
            messages=messages,
            deployment_id="gpt-35-turbo",
            function_call="none",
            functions=functions,
            temperature=0
        )

        answer = response['choices'][0]['message']
    else:
      answer = response_message
  
  elif arbitration_method == AribitrationMethod.SEMANTIC_KERNEL.value:
    my_logger = sk.NullLogger()
    kernel = sk.Kernel(log=my_logger)
    kernel.add_text_completion_service("dv", AzureChatCompletion("gpt-35-turbo", llm_connection.api_base, llm_connection.api_key))

    kernel.create_semantic_function(
      intent_prompt,
      description="Gets the intent of the user",
      function_name="GetIntent",
      skill_name="OrchestratorPlugin"
    )

    kernel.create_semantic_function(
      format_response,
      description="Takes a question and answer and formats it in a human readable way",
      function_name="FormatResponse",
      skill_name="OrchestratorPlugin"
    )


    # For each tool, import the skills (can we do this?)

    native_funcs = {}
    for tool in flow_tools:
      print(f"Loading skill: {tool.name}")
      native_funcs[tool.name] = tool.to_sk_function()
    kernel.import_skill(native_funcs, "FlowPlugin")
    
    orchestratorPlugin = kernel.import_skill(
        OrchestratorPlugin(kernel), "OrchestratorPlugin"
    )
    print("Calling Orchestrator")
    result = orchestratorPlugin["route_request"].invoke(
        query
    )

    print(f"This is result: {result}")
    answer = result["input"]

  return answer

