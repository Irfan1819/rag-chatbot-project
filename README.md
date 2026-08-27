# AI Projects: RAG Document Q&A + Multi-Tool AI Agent

This repository contains two AI applications built with Python and the Groq API:

1. **RAG Document Q&A Chatbot** — answers questions grounded in your own documents
2. **Multi-Tool AI Agent** — an AI agent that autonomously decides when to use tools like weather lookup, web search, a calculator, and date/time

---

## 1. RAG Document Q&A Chatbot

A command-line and web-based application that answers questions based on your own documents using Retrieval-Augmented Generation (RAG). Instead of relying only on general AI knowledge, this tool retrieves the most relevant information from your files before generating an answer.

### How it works

1. Loads and splits text documents into chunks
2. Converts each chunk into an embedding (a numerical representation of its meaning) using `sentence-transformers`
3. When you ask a question, it finds the top 3 most relevant chunks using cosine similarity
4. Sends your question + the retrieved context to an LLM (via Groq API) to generate a grounded answer

### Interface

- **Terminal version** (`document_qa.py`) — command-line chat interface
- **Web version** (`app.py`) — browser-based chat interface built with Streamlit

### Run it

```
python document_qa.py
```
or
```
streamlit run app.py
```

### Example

```
You: What is RAG?
AI: RAG, or Retrieval-Augmented Generation, is a technique where an AI model retrieves relevant information from a knowledge base before generating an answer, making responses more accurate and grounded in real data.
```

---

## 2. Multi-Tool AI Agent

An AI agent (`agent.py`) that autonomously decides which tool(s) to use to answer a question, rather than following a fixed script. It can chain multiple tools together to answer compound questions, remembers conversation context across turns, and includes safeguards against common failure modes in tool-calling systems.

### Tools available to the agent

- **Calculator** — evaluates math expressions
- **Weather lookup** — gets current weather for any city (OpenWeatherMap API)
- **Date/time** — returns the current date and time
- **Web search** — searches the web for current information (Tavily API)

### Key features

- **Autonomous tool selection** — the agent decides on its own whether a question needs a tool, and which one
- **Multi-step reasoning** — chains multiple tool calls together for compound questions (e.g., comparing weather in two cities)
- **Conversation memory** — remembers earlier questions and answers, so follow-up questions with pronouns ("is that hot?") resolve correctly
- **Safety limits** — caps the number of tool calls per question to prevent infinite loops
- **Error handling** — gracefully recovers from malformed model outputs instead of crashing
- **Hallucination grounding** — explicitly instructed to only state facts present in tool/search results, and to say so when information is incomplete, rather than inventing details

### Run it

```
python agent.py
```

### Example

```
You: What's the weather in Tokyo and Paris, and which one is warmer?
[Agent decided to use tool: get_weather with {'city': 'Tokyo'}]
[Agent decided to use tool: get_weather with {'city': 'Paris'}]
AI: Tokyo: 33.23°C, broken clouds
    Paris: 21.94°C, scattered clouds
    Tokyo is warmer than Paris.
```

---

## Tech stack

- Python
- Groq API (LLM inference)
- sentence-transformers (embeddings)
- NumPy (similarity calculations)
- Streamlit (web interface)
- Tavily API (web search)
- OpenWeatherMap API (weather data)

## Setup

1. Clone this repo
2. Install dependencies:

```
pip install groq python-dotenv sentence-transformers numpy streamlit requests tavily-python
```

3. Create a `.env` file with your API keys:

```
GROQ_API_KEY=your-groq-key-here
WEATHER_API_KEY=your-openweathermap-key-here
TAVILY_API_KEY=your-tavily-key-here
```

4. For the RAG project: add `.txt` files to the `documents/` folder
5. Run whichever project you want (see "Run it" sections above)

## What I learned

Built these projects to learn the fundamentals of applied AI development:
- **RAG systems** — chunking, embeddings, semantic search, and grounding LLM responses in external data
- **AI agents** — function/tool calling, multi-step reasoning, conversation memory, and the real engineering challenges of building reliable agentic systems (handling malformed model outputs, preventing infinite loops, and reducing hallucination even when tools are used)
- Building simple web interfaces for AI applications using Streamlit
- Secure API key handling using environment variables
