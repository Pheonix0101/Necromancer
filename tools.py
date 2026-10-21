from datetime import datetime
import requests
from Utilities.utilities import log
import json


def get_current_time():
    return datetime.now()

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url,timeout=5)
    response.raise_for_status()     # This will raise Https error
    return response.text

def get_user_city():
    return 'bangalore'


TOOLS = [
    {
        "type":"function",
        "function":{
            "name": "get_current_time",
            "description": "Returns the current time and date as a well formatted manner.",
            "parameters": {"type":"object", "properties":{},},
        },
    },
    {
        "type":"function",
        "function":{
            "name":"get_city_weather",
            "description": "Returns the current weather of given city.",
            "parameters": {
                "type":"object", 
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"city to get weather info.",
                    }
                },
                "required": ["city"]
            },
        }
    },
    {
        "type":"function",
        "function":{
            "name": "get_user_city",
            "description": "Returns the city where user live. use this when user say 'my city', 'where i live', or 'my location' without naming the city.",
            "parameters": {"type":"object", "properties":{},},
        },
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP={
    "get_current_time":get_current_time,
    "get_city_weather":get_city_weather,
    "get_user_city": get_user_city,
}    


def run_tool(tool_call):
    func_name = tool_call.function.name
    func_args = {}
    
    try:
        func_args = json.loads(tool_call.function.arguments or "{}")
        log(f"🛠️ {func_name}({func_args})")
        fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
        result = fn(**func_args)
    except Exception as e:
        result = f"Error while running {func_name}: {e}"
    
    log(f"   🍺 {result}")
    return str(result)