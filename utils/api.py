from google import genai
from google.genai import types
import time
from rich.console import Console
from utils.key_manager import ApiKeyManager

# Initialize Rich console for this module
console = Console()

def initialize_client():
    """Initialize and return a Google GenAI client with API key from environment"""
    # Use the ApiKeyManager to get the Gemini API key
    key_manager = ApiKeyManager(required_keys=["GEMINI_API_KEY"], console=console)
    GEMINI_API_KEY = key_manager.get("GEMINI_API_KEY")

    # Set up the API key for Google GenAI
    with console.status("[bold blue]Setting up Google GenAI client...", spinner="bouncingBar"):
        client = genai.Client(api_key=GEMINI_API_KEY)
        console.print("[bold green]Client initialized successfully![/bold green]")
        
    return client

def count_tokens(client, model, contents):
    """Count tokens in the given contents using the specified model"""
    with console.status("[bold cyan]Counting tokens...", spinner="dots"):
        tokens = client.models.count_tokens(model=model, contents=contents)
    return tokens.total_tokens

def generate_response(client, model, query, temperature=1.0):
    """Generate a response from the model for the given query"""
    # Count tokens first
    token_count = count_tokens(client, model, query)
    
    # Generate the response and time it
    start_time = time.time()
    response = client.models.generate_content(
        model=model, 
        contents=query,
        config=types.GenerateContentConfig(
            temperature=temperature,
        ),
    )
    elapsed_time = time.time() - start_time
    
    return response, token_count, elapsed_time