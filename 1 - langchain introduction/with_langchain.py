from langchain_groq import ChatGroq
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Groq setup with LangChain (FREE & FAST!)
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
)

# Just three lines! Memory is handled automatically
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# Using it is this simple!
response = conversation.predict(input="Hello! My name is Wali")
print(response)

response = conversation.predict(input="What is my name?")
print(response)
