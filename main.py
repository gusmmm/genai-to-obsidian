from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.tree import Tree
from rich.table import Table
from utils.api import initialize_client, generate_response, count_tokens
from utils.display import (setup_console, display_model_info, display_token_info, 
                          display_query, show_response, show_details, 
                          show_completion_time)
import time

def main():
    # Initialize API client
    client = initialize_client()
    
    # Configuration
    model = 'gemini-2.0-flash-thinking-exp-01-21'
    query = "What are the main chemical, physical and organic characteristics in a system that can be considered as 'alive'?"
    temperature = 1.0
    
    # Display Intro
    setup_console()
    
    # Display model information
    display_model_info(model)
    
    # Display the query in a panel
    display_query(query)
    
    # Count tokens and display token info
    token_count = count_tokens(client, model, query)
    display_token_info(token_count)
    
    # Show a progress spinner while waiting for the response
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Generating response from Gemini...[/bold blue]"),
        BarColumn(),
        TimeElapsedColumn(),
        transient=False
    ) as progress:
        task = progress.add_task("Generating", total=None)
        
        # Make the API call inside the progress context
        response, token_count, elapsed_time = generate_response(client, model, query, temperature)
        progress.update(task, completed=100)
    
    # Display the response in a nice panel with markdown formatting
    show_response(response.text)
    
    # Display detailed information as a tree
    show_details(model, temperature, token_count, elapsed_time, response)

if __name__ == "__main__":
    start_time = time.time()
    main()
    show_completion_time(start_time)