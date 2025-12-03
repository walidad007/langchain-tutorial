from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Groq client setup (FREE API!)
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Manual conversation management
conversation_history = []


def chat_without_langchain(user_message):
    # Declare that we intend to modify the global variable
    global conversation_history

    global client  # Although client likely won't change, it's good practice

    # Manually append user message
    conversation_history.append({"role": "user", "content": user_message})

    # Must count tokens manually
    total_tokens = sum(len(msg["content"].split()) for msg in conversation_history)

    # If tokens exceed limit, must trim manually
    if total_tokens > 3000:
        conversation_history = conversation_history[-10:]

    # API call with Groq - SUPER FAST & FREE!
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history,
        temperature=0.7,
        max_tokens=1024,
    )

    # Extract the response
    assistant_message = response.choices[0].message.content

    # Manually append assistant message
    conversation_history.append({"role": "assistant", "content": assistant_message})

    return assistant_message


# Using the function
response = chat_without_langchain("Hello! My is Wali")
print(response)

response = chat_without_langchain("What is my name?")
print(response)
