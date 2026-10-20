from datetime import datetime
import requests


def get_current_time():
    return datetime.now()

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url,timeout=5)
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