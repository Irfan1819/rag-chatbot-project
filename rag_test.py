from sentence_transformers import SentenceTransformer

model=SentenceTransformer('all-MiniLM-L6-v2')

with open("notes.txt","r") as file:
    text=file.read()

chunks=[chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


print(f"Document split into {len(chunks)} chunks:\n")

for i, chunk in enumerate(chunks):
    print(f"Chunk {i}:{chunk[:60]}...")

embeddings=model.encode(chunks)

print(f"\nEach chunk is now a vector of {len(embeddings[0])} numbers.")

print(f"Example — first 5 numbers of Chunk 0's embedding: {embeddings[0][:5]}")

import numpy as np
from numpy.linalg import norm

def find_most_relevant_chunk(question, chunks, embeddings, model):
    question_embedding = model.encode([question])[0]
    
    # Calculate similarity between the question and every chunk
    similarities = []
    for chunk_embedding in embeddings:
        similarity = np.dot(question_embedding, chunk_embedding) / (norm(question_embedding) * norm(chunk_embedding))
        similarities.append(similarity)
    
    # Find the chunk with the highest similarity score
    best_index = np.argmax(similarities)
    return chunks[best_index], similarities[best_index]

# Test it
question = "What are lists in Python?"
best_chunk, score = find_most_relevant_chunk(question, chunks, embeddings, model)

print(f"\nQuestion: {question}")
print(f"Most relevant chunk (similarity: {score:.3f}):")
print(best_chunk)