# ============================================================================
# PROBLEM #1: The 100-Line "Hello World" Chatbot
# Video mein gradually type karte hue dikhana hai
# ============================================================================

# Step 1: API client setup karna
from groq import Groq
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize client
client = Groq(api_key=groq_api_key)


# Step 2: Conversation history store karna
conversation_history = []
max_history_length = 10


# Step 3: Token counting function
def count_tokens(text):
    """Simple token counter (rough estimate)"""
    return len(text.split())


def get_total_tokens():
    """Calculate total tokens in conversation"""
    total = 0
    for msg in conversation_history:
        total += count_tokens(msg["content"])
    return total


# Step 4: Context management
def manage_context():
    """Trim conversation if it exceeds token limit"""
    max_tokens = 3000

    while get_total_tokens() > max_tokens and len(conversation_history) > 2:
        # Remove oldest messages (keep system message if any)
        if conversation_history[0]["role"] == "system":
            conversation_history.pop(1)
        else:
            conversation_history.pop(0)

    # Also limit by message count
    if len(conversation_history) > max_history_length:
        conversation_history[:] = conversation_history[-max_history_length:]


# Step 5: Rate limiting handler
last_request_time = None
min_request_interval = 1.0  # seconds


def handle_rate_limit():
    """Ensure we don't exceed rate limits"""
    global last_request_time

    if last_request_time:
        elapsed = time.time() - last_request_time
        if elapsed < min_request_interval:
            time.sleep(min_request_interval - elapsed)

    last_request_time = time.time()


# Step 6: Error handling wrapper
def make_api_call_with_retry(messages, max_retries=3):
    """Make API call with retry logic"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                timeout=30,
            )
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2**attempt)  # Exponential backoff


# Step 7: Response parsing and validation
def parse_response(response):
    """Extract and validate response"""
    try:
        if not response.choices:
            raise ValueError("No response choices received")

        message = response.choices[0].message

        if not message.content:
            raise ValueError("Empty response content")

        return message.content.strip()

    except Exception as e:
        print(f"Error parsing response: {e}")
        return None


# Step 8: Main chat function
def chat_without_langchain(user_message):
    """
    Complete chatbot function - ALL MANUAL!
    Line count: 100+
    """

    # Validate input
    if not user_message or not user_message.strip():
        return "Error: Empty message"

    # Add user message to history
    conversation_history.append(
        {
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat(),
        }
    )

    # Manage context (trim if needed)
    manage_context()

    # Check token limits
    current_tokens = get_total_tokens()
    print(f"Current tokens: {current_tokens}")

    # Handle rate limiting
    handle_rate_limit()

    # Prepare messages for API
    api_messages = [
        {"role": msg["role"], "content": msg["content"]} for msg in conversation_history
    ]

    try:
        # Make API call with retry
        response = make_api_call_with_retry(api_messages)

        # Parse response
        assistant_message = parse_response(response)

        if not assistant_message:
            return "Error: Failed to parse response"

        # Add assistant response to history
        conversation_history.append(
            {
                "role": "assistant",
                "content": assistant_message,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Log for debugging
        print(f"Response received: {len(assistant_message)} characters")
        print(f"Total messages: {len(conversation_history)}")

        return assistant_message

    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)

        # Log error
        with open("chat_errors.log", "a") as f:
            f.write(f"{datetime.now()}: {error_message}\n")

        return "Sorry, an error occurred. Please try again."


# Step 9: Helper functions for conversation management
def get_conversation_summary():
    """Get summary of current conversation"""
    return {
        "total_messages": len(conversation_history),
        "total_tokens": get_total_tokens(),
        "user_messages": len([m for m in conversation_history if m["role"] == "user"]),
        "assistant_messages": len(
            [m for m in conversation_history if m["role"] == "assistant"]
        ),
    }


def clear_conversation():
    """Clear conversation history"""
    conversation_history.clear()
    print("Conversation cleared")


def export_conversation(filename="conversation.txt"):
    """Export conversation to file"""
    with open(filename, "w", encoding="utf-8") as f:
        for msg in conversation_history:
            f.write(f"{msg['role'].upper()}: {msg['content']}\n")
            f.write(f"Time: {msg.get('timestamp', 'N/A')}\n")
            f.write("-" * 50 + "\n")


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    print("🤖 Chatbot Without LangChain")
    print("=" * 50)
    print(f"Total lines of code: 100+")
    print("=" * 50)

    # Test conversation
    response1 = chat_without_langchain("Hello! My name is Wali.")
    print(f"\nUser: Hello! My name is Wali.")
    print(f"Bot: {response1}")

    print("\n" + "=" * 50)

    response2 = chat_without_langchain("What is my name?")
    print(f"\nUser: What is my name?")
    print(f"Bot: {response2}")

    print("\n" + "=" * 50)
    print("\n📊 Conversation Summary:")
    summary = get_conversation_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 50)
    print("😤 All this code... just for basic chat!")
    print("=" * 50)
