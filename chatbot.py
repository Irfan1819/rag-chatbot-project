import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
conversation = []
print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    user_input=input("You: ")
    if user_input.lower() =="quit":
        print("Goodbye!")
        break


    conversation.append({"role": "user", "content": user_input})
    
    # Send the ENTIRE conversation so far to the AI
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_tokens=500,
        messages=conversation
    )
    
    ai_reply = response.choices[0].message.content
    print("AI:", ai_reply)
    
    # Add the AI's reply to the conversation history too
    conversation.append({"role": "assistant", "content": ai_reply})
