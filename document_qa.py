import os
import glob
import numpy as np
from numpy.linalg import norm
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = SentenceTransformer('all-MiniLM-L6-v2')


# Load and chunk ALL .txt documents in the "documents" folder
chunks = []
chunk_sources = []  # keeps track of which file each chunk came from

for filepath in glob.glob("documents/*.txt"):
    with open(filepath, "r") as file:
        text = file.read()
    file_chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    chunks.extend(file_chunks)
    chunk_sources.extend([filepath] * len(file_chunks))

embeddings = model.encode(chunks)
print(f"Loaded {len(chunks)} chunks from {len(glob.glob('documents/*.txt'))} document(s).\n")


def find_relevant_chunks(question, top_n=3):
    question_embedding = model.encode([question])[0]
    similarities = [
        np.dot(question_embedding, c) / (norm(question_embedding) * norm(c))
        for c in embeddings
    ]
    top_indices = np.argsort(similarities)[::-1][:top_n]
    return [chunks[i] for i in top_indices]

while True:
    question = input("You: ")
    if question.lower() == "quit":
        print("Goodbye!")
        break
    
    relevant_chunks = find_relevant_chunks(question)
    context = "\n\n".join(relevant_chunks)  # join multiple chunks together
    
    prompt = f"""Answer the question based only on the context below. 
If the answer isn't in the context, say "I don't know based on the document."

Context: {context}

Question: {question}"""
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    print("AI:", response.choices[0].message.content)
    print()