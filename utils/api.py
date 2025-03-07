from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time
from rich.console import Console

# Initialize Rich console for this module
console = Console()

def initialize_client():
    """Initialize and return a Google GenAI client with API key from environment"""
    with console.status("[bold blue]Loading environment variables...", spinner="dots"):
        load_dotenv()
        # Ensure you have set the GEMINI_API_KEY in your .env file
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            console.print("[bold red]Error:[/bold red] GEMINI_API_KEY not found. Please check your .env file.", style="bold red")
            raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")
        else:
            console.print("[bold green]API Key loaded successfully![/bold green]")

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
    """Generate a response from the model for the given query
    
    Args:
        client: The GenAI client
        model (str): The model ID to use
        query (str): The query to send to the model
        temperature (float): Temperature parameter for generation
        
    Returns:
        tuple: (response, token_count, elapsed_time)
    """
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