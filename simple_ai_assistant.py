from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import json
import os

load_dotenv();

client = OpenAI(
base_url= os.getenv("BASE_URL"),
api_key= os.getenv("API_KEY")
);

MAX_STEPS = 5
messages = []

messages.append({
    "role":"system",
    "content":"Act like a very humble agent and respond alwayse under 20 words"
})

while True:
    user_input = input("\nPheonix: ")    
    if user_input.lower() in ["exit","quit","band","tata"]:
        break

    messages.append({"role": "user", "content": user_input})

    # chained tool calling
    for steps in range(MAX_STEPS):

        response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools=TOOLS
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = {}

            try:
                func_args = json.loads(tool_call.function.arguments or "{}")
                fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result = fn(**func_args)
            except Exception as e:
                result = f"Error while running {func_name}: {e}"

            messages.append({
                "role":"tool",
                "tool_id":"tool_call.id",
                "content": str(result),
            })
    else:
        # ran out of steps: The model never gave he final answer.
        fallback= "Sorry, I could not finish this within the steps limit."
        messages.append({
            "role":"assistant",
            "content":fallback
        })
        print("Assistant: "+ fallback)
        continue


    messages.append({
        "role":"assistant",
        "content":"msg.content"
    })

    print("Assistant: "+ msg.content)


