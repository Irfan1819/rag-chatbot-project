import os
import glob
import numpy as np
from numpy.linalg import norm
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import streamlit as st


load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def load_documents():
    model=load_model()

    chunks=[]

    for filepath in glob.glob("documents/*.txt"):
        with open(filepath,"r") as file:
            text = file.read()
        file_chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
        chunks.extend(file_chunks)
    embeddings = model.encode(chunks)
    return chunks, embeddings

model = load_model()
chunks, embeddings = load_documents()

def find_relevant_chunks(question, top_n=3):
    question_embedding = model.encode([question])[0]
    similarities = [
        np.dot(question_embedding, c) / (norm(question_embedding) * norm(c))
        for c in embeddings
    ]
    top_indices = np.argsort(similarities)[::-1][:top_n]
    return [chunks[i] for i in top_indices]

# --- Web UI starts here ---
st.title("📄 Document Q&A Chatbot")
st.write("Ask questions about the documents in your knowledge base.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask a question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    relevant_chunks = find_relevant_chunks(question)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""Answer the question based only on the context below. 
If the answer isn't in the context, say "I don't know based on the document."

Context: {context}

Question: {question}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)


