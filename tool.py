from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv()
'''
1. get_weather(city)
Purpose: Fetches real-time weather data for a given city using the OpenWeather API.
What it does:
-Sends a request to the OpenWeather service.
-Returns a weather description and temperature in Celsius.
-Requires a valid API key stored in the .env file.
'''
def get_weather(city):
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"The weather in {city} is {desc} with a temperature of {temp}°C."
    else:
        return f"Could not retrieve weather data for {city}."



'''
2. search_web(query)
Purpose: Performs live web searches using DuckDuckGo.
What it does:
-Takes a user's query as input.
-Uses the DuckDuckGoSearchRun tool to return summarized web results.
-Ideal for quick facts, current events, or general information lookup.
'''
search_tool = DuckDuckGoSearchRun()

def search_web(query: str) -> str:
    # Use the search tool to perform the query
    results = search_tool.run(query)
    return results

'''
3. save_to_txt(data, filename="research_output.txt")
Purpose: Saves structured text data to a local file.
What it does:
-Appends the given content to a text file.
-Includes a timestamp for traceability.
-Useful for logging research results or preserving assistant output for later review.
'''
def save_to_txt(data: str, filename: str = "output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"


save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

