from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from tool import search_web, get_weather, save_to_txt
import json

# Step 1: Load API token
load_dotenv()
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Step 2: Get user input
user_input = input("Ask the assistant something: ").strip()

# Step 3: Prepare prompt
system_prompt = """
You are an assistant that can call tools like search_web() and get_weather().
Decide which tool to use based on the user question.

Respond only with a JSON object like this:
{"action": "search_web", "input": "<query>"}

Available actions:
- search_web
- get_weather
"""

prompt=f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}
<|eot_id|><|start_header_id|>user<|end_header_id|>
{user_input}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""



# Step 4: Call model
client = InferenceClient(token=token,model="HuggingFaceH4/zephyr-7b-beta")

action_blob = client.text_generation(
    prompt=prompt,
    max_new_tokens=30,
)

print(action_blob)


def format_response(tool_name: str, query: str, summary: str) -> str:
    # Limit summary length to first 300 characters to keep it concise
    truncated_summary = summary[:300] + "..." if len(summary) > 300 else summary

    response = (
        f"Tool used: {tool_name}\n"
        f"Query: {query}\n"
        f"Summary:\n{truncated_summary}"
    )
    return response



try:
    action_data = json.loads(action_blob)

    action = action_data.get("action")
    argument = action_data.get("input")

    if action == "search_web":
        result = search_web(argument)
    elif action == "get_weather":
        result = get_weather(argument)
    else:
        result = f"Unknown action: {action}"

    print(format_response(action, user_input, result))
    save_to_txt(format_response(action, user_input, result))

except json.JSONDecodeError:
    print("Failed to parse JSON from model output.")