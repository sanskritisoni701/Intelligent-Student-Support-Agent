
import os
from dotenv import load_dotenv
from groq import Groq

# Step 1: Load environment variables from .env
load_dotenv()

# Step 2: Retrieve API key and model name
api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL")

# Step 3: Check whether API key exists
if not api_key:
    raise ValueError("Groq API key not found. Check your .env file.")

# Step 4: Connect to Groq
client = Groq(api_key=api_key)

# Step 5: Send a question to the AI model
response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": "Explain what an AI agent is in simple words."
        }
    ]
)

# Step 6: Display the AI response
print("\nAI RESPONSE:")
print(response.choices[0].message.content)

# Step 7: Display token usage
print("\nTOKEN USAGE:")
print("Input tokens:", response.usage.prompt_tokens)
print("Output tokens:", response.usage.completion_tokens)
