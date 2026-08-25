#  RAG Document Q&A Chatbot

A command-line application that answers questions based on your own documents using 
Retrieval-Augmented Generation (RAG). Instead of relying only on general AI knowledge, 
this tool retrieves the most relevant information from your files before generating an answer.

##  How it works

1. Loads and splits text documents into chunks
2. Converts each chunk into an embedding (a numerical representation of its meaning) using `sentence-transformers`
3. When you ask a question, it finds the top 3 most relevant chunks using cosine similarity
4. Sends your question + the retrieved context to an LLM (via Groq API) to generate a grounded answer

##  Tech stack

- Python
- Groq API (LLM inference)
- sentence-transformers (embeddings)
- NumPy (similarity calculations)


##  Setup

1. Clone this repo
2. Install dependencies:

pip install groq python-dotenv sentence-transformers numpy

3. Create a `.env` file with your Groq API key:

GROQ_API_KEY=your-key-here

4. Add `.txt` files to the `documents/` folder
5. Run the app:

python document_qa.py

##  Example

You: What is RAG?

AI: RAG, or Retrieval-Augmented Generation, is a technique where an AI model retrieves relevant information from a knowledge base before generating an answer...
