# 🧠 Tool-Calling Assistant using Hugging Face Zephyr

This is a simple Python assistant that uses [Hugging Face's](https://huggingface.co) `zephyr-7b-beta` model to interpret user input and decide whether to:

- 🔍 Search the web
- ☁️ Get weather data

The assistant automatically selects the appropriate tool based on the input, executes the tool, and presents a summarized result.

---

## ✨ Features

- Natural language input
- Automated tool selection (`search_web`, `get_weather`)
- Result display and logging
- Built with Hugging Face Inference API

---

## 📦 Requirements

Before running, make sure you have Python 3.8+ and install dependencies:

```bash
pip install huggingface_hub python-dotenv
```

Also, you should create a .env file with your Hugging Face API token:
```bash
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

## 📦 Project Structure
```
.
├── main.py             # Main assistant logic
├── tool.py             # Custom tool functions
├── .env                # Contains your Hugging Face API key (not tracked)
└── README.md           # This file
```

## 🚀 How to Run
```
python main.py
```
Then enter a question like:
```
What's the weather in Taipei?

Who won the last World Cup?
```
The model will respond with a tool call like:
```
{"action": "search_web", "input": "last World Cup winner"}
```
The program will:

Parse the JSON

Call the appropriate tool

Show a response like:
```
Tool used: search_web
Query: Who won the last World Cup?
Summary:
Argentina won the 2022 FIFA World Cup after defeating France in the final match...
```

It also saves the result to a .txt file automatically.
