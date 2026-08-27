# RAG Document Q&A Chatbot

A command-line and web-based application that answers questions based on your own documents using Retrieval-Augmented Generation (RAG). Instead of relying only on general AI knowledge, this tool retrieves the most relevant information from your files before generating an answer.

> Looking for my AI agent project (tool calling, multi-step reasoning)? That now lives in a separate repo: [ai-tool-agent](https://github.com/Irfan1819/ai-tool-agent)

## How it works

1. Loads and splits text documents into chunks
2. Converts each chunk into an embedding (a numerical representation of its meaning) using `sentence-transformers`
3. When you ask a question, it finds the top 3 most relevant chunks using cosine similarity
4. Sends your question + the retrieved context to an LLM (via Groq API) to generate a grounded answer

## Interface

This project includes three ways to interact with it:

- **Terminal version** (`document_qa.py`) — command-line chat interface, supports multiple documents with top-3 retrieval
- **Web version** (`app.py`) — browser-based chat interface built with Streamlit
- **Memory chatbot** (`chatbot.py`) — an earlier, simpler version demonstrating conversation memory without document retrieval

## Tech stack

- Python
- Groq API (LLM inference)
- sentence-transformers (embeddings)
- NumPy (similarity calculations)
- Streamlit (web interface)

## Setup

1. Clone this repo
2. Install dependencies:

```
pip install groq python-dotenv sentence-transformers numpy streamlit
```

3. Create a `.env` file with your Groq API key:

```
GROQ_API_KEY=your-key-here
```

4. Add `.txt` files to the `documents/` folder
5. Run the app:

- Terminal version (multi-document RAG):
```
python document_qa.py
```

- Web version:
```
streamlit run app.py
```

- Simple memory chatbot (no document retrieval):
```
python chatbot.py
```

## Example

```
You: What is RAG?
AI: RAG, or Retrieval-Augmented Generation, is a technique where an AI model retrieves relevant information from a knowledge base before generating an answer, making responses more accurate and grounded in real data.
```

## What I learned

Built this project to learn the fundamentals of RAG systems — chunking, embeddings, semantic search, and grounding LLM responses in external data. Also learned how to build a simple web interface for an AI application using Streamlit, and how to handle API keys securely using environment variables.
