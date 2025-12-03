from langchain_classic.agents import initialize_agent, Tool, AgentType
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Groq LLM setup
llm = ChatGroq(
    groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile", temperature=0
)

# Wikipedia tool setup
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# Define the tools the agent can use
tools = [
    Tool(
        name="Wikipedia", func=wikipedia.run, description="Use this to search Wikipedia"
    )
]

# Initialize the agent using the simple, classic function
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Use the proper Enum
    verbose=True,
)

# Agent will decide on its own whether to use Wikipedia
response = agent.run("what is the capital of pakistan and how much population of it?")
print(response)
