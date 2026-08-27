import os
import requests
from datetime import datetime
from tavily import TavilyClient
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))



# --- Define our actual tool functions ---

def calculate(expression):
    """Safely evaluates a basic math expression."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error calculating: {e}"
    


def get_weather(city):
    """Gets current weather for a city."""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data.get("cod") != 200:
        return f"Could not find weather for {city}"
    
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    return f"Temperature in {city}: {temp}°C, {description}"

def get_current_datetime():
    """Returns the current date and time."""
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y - %I:%M %p")


def web_search(query):
    """Searches the web for current information."""
    try:
        results = tavily_client.search(query, max_results=3)
        summaries = []
        for result in results["results"]:
            summaries.append(f"- {result['title']}: {result['content'][:500]}")
        return "\n".join(summaries)
    except Exception as e:
        return f"Search failed: {e}"


# --- Describe these tools to the AI (so it knows they exist) ---

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a math expression, e.g. '5 + 3' or '10 * 2'",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. 'Tokyo'"
                    }
                },
                "required": ["city"]
            }
        }
    },

        
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }

        ,
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information, news, or facts not otherwise known",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }

]

# --- Map tool names to actual functions ---

available_functions = {
    "calculate": calculate,
    "get_weather": get_weather,
    "get_current_datetime": get_current_datetime,
    "web_search": web_search
}

print("AI Agent ready! Type 'quit' to exit.\n")

# This now lives OUTSIDE the loop, so it persists across questions
messages = [{"role": "system", "content": "When using search results or tool outputs, only state facts that are explicitly present in those results. Never invent specific dates, numbers, names, or events. If information is incomplete, say so clearly. For questions that require multiple steps or multiple pieces of information, briefly state your plan first (e.g., 'I'll check the weather, then calculate...') before using tools."}]
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    messages.append({"role": "user", "content": user_input})
    # Keep looping as long as the AI wants to call tools
    max_iterations = 5
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                tools=tools
            )
        except Exception as e:
            print(f"[Tool call issue occurred, asking AI to answer with what it has]")
            fallback_response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages + [{"role": "user", "content": "Please just answer based on what you know so far, without using any more tools."}]
            )
            print("AI:", fallback_response.choices[0].message.content)
            break

        response_message = response.choices[0].message

        if response_message.tool_calls:
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"[Agent decided to use tool: {function_name} with {function_args}]")

                function_to_call = available_functions[function_name]
                function_result = function_to_call(**function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": function_result
                })
            continue
        else:
            print("AI:", response_message.content)
            messages.append({"role": "assistant", "content": response_message.content})
            break
    else:
        final_attempt = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages + [{"role": "user", "content": "Based ONLY on the actual search results above, summarize what you found. Do not invent details, dates, numbers, or events that weren't explicitly in the search results. If the results are limited or unclear, say so honestly rather than filling in gaps."}]
        )
        print("AI:", final_attempt.choices[0].message.content)
        messages.append({"role": "assistant", "content": final_attempt.choices[0].message.content})