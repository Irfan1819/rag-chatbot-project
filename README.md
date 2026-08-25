RAG Document Q&A Chatbot

A command-line and web-based application that answers questions based on your own documents using Retrieval-Augmented Generation (RAG). Instead of relying only on general AI knowledge, this tool retrieves the most relevant information from your files before generating an answer.

How it works
Loads and splits text documents into chunks
Converts each chunk into an embedding (a numerical representation of its meaning) using sentence-transformers
When you ask a question, it finds the top 3 most relevant chunks using cosine similarity
Sends your question + the retrieved context to an LLM (via Groq API) to generate a grounded answer
Interface

This project includes two ways to interact with it:

Terminal version (document_qa.py) — command-line chat interface
Web version (app.py) — browser-based chat interface built with Streamlit
Tech stack
Python
Groq API (LLM inference)
sentence-transformers (embeddings)
NumPy (similarity calculations)
Streamlit (web interface)
Setup
Clone this repo
Install dependencies:
pip install groq python-dotenv sentence-transformers numpy streamlit
Create a .env file with your Groq API key:
GROQ_API_KEY=your-key-here
Add .txt files to the documents/ folder
Run the app:
Terminal version:
python document_qa.py
Web version:
streamlit run app.py
Example
You: What is RAG?
AI: RAG, or Retrieval-Augmented Generation, is a technique where an AI model retrieves relevant information from a knowledge base before generating an answer, making responses more accurate and grounded in real data.
What I learned

Built this project to learn the fundamentals of RAG systems — chunking, embeddings, semantic search, and grounding LLM responses in external data. Also learned how to build a simple web interface for an AI application using Streamlit, and how to handle API keys securely using environment variables.
