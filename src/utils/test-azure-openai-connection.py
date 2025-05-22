import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from pyprojroot import here
import sys
# Add the root of the project (where `src/` lives) to sys.path
sys.path.append(str(here()))

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")  # Update this to your API version
deployment_name = os.getenv("AZURE_MODEL_DEPLOYMENT_NAME")  # Replace with your deployment name

# Validate environment variables
if not api_key or not endpoint:
    raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT in environment variables.")

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

# Define the prompt
prompt = "Write a short peom on materails synthesis."

# Create a chat completion request
try:
    print("Sending a test completion job...")
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )
    # Extract and print the response
    message = response.choices[0].message.content.strip()
    print(f"Prompt: {prompt}\nResponse: {message}")
except Exception as e:
    print(f"An error occurred: {e}")
