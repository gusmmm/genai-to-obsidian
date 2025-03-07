from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.tree import Tree
from rich.table import Table
from utils.api import initialize_client, generate_response, count_tokens
import time

# Initialize Rich console
console = Console()

def display_token_info(token_count):
    """Display token count information in a table"""
    token_table = Table(title="Token Information")
    token_table.add_column("Metric", style="cyan")
    token_table.add_column("Value", style="green")
    token_table.add_row("Total Tokens", str(token_count))
    console.print(token_table)
    return token_count

def display_model_info(model):
    """Display information about the selected model"""
    model_info = Table(title="Model Information")
    model_info.add_column("Property", style="cyan")
    model_info.add_column("Value", style="green")
    model_info.add_row("Model ID", model)
    console.print(model_info)

def main():
    # Initialize API client
    client = initialize_client()
    
    # Configuration
    model = 'gemini-2.0-flash-thinking-exp-01-21'
    query = "Why am I alive?"
    temperature = 1.0
    
    # Display Intro
    console.rule("[bold purple]🤖 Gemini API Interaction[/bold purple]")
    
    # Display model information
    display_model_info(model)
    
    # Display the query in a panel
    console.print(Panel(f"[bold yellow]Query:[/bold yellow] {query}", 
                       title="Input", 
                       border_style="yellow"))
    
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
    console.print("\n")
    console.print(Panel(
        Markdown(response.text),
        title="[bold green]Gemini Response[/bold green]",
        border_style="green",
        expand=False
    ))
    
    # Display detailed information as a tree
    details = Tree("[bold cyan]Request Details[/bold cyan]")
    details.add("[cyan]Model:[/cyan] " + model)
    details.add("[cyan]Temperature:[/cyan] " + str(temperature))
    details.add("[cyan]Token count:[/cyan] " + str(token_count))
    details.add(f"[cyan]Response time:[/cyan] {elapsed_time:.3f} seconds")
    
    # Attempt to extract safety ratings if available
    safety_node = details.add("[cyan]Safety Ratings:[/cyan]")
    try:
        if hasattr(response, 'candidates') and response.candidates:
            for rating in response.candidates[0].safety_ratings or []:
                safety_node.add(f"[yellow]{rating.category}:[/yellow] {rating.probability}")
    except (AttributeError, IndexError):
        safety_node.add("[yellow]No safety ratings available[/yellow]")
        
    console.print(details)

if __name__ == "__main__":
    console.rule("[bold purple]Gemini API Demo[/bold purple]")
    start_time = time.time()
    main()
    elapsed = time.time() - start_time
    console.rule(f"[bold purple]Completed in {elapsed:.2f} seconds[/bold purple]")