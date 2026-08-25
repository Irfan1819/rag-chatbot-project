import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client=Groq(api_key=os.getenv("GROP_API_KEY"))

response= client.chat.completions.create(model="openai/gpt-oss-120b",max_tokens=200,messages=[{
    "role":"user","content":"Explain what an API is, in 2 senetences"
}
]
)

print(response.choices[0].message.content)