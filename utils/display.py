from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.tree import Tree
from rich.table import Table
import time

# Initialize Rich console
console = Console()

def setup_console():
    """Setup the Rich console and return it"""
    console.rule("[bold purple]🤖 Gemini API Interaction[/bold purple]")
    return console

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

def display_query(query):
    """Display the query in a panel"""
    console.print(Panel(
        f"[bold yellow]Query:[/bold yellow] {query}", 
        title="Input", 
        border_style="yellow"
    ))

def show_response(response_text):
    """Display the response in a markdown panel"""
    console.print("\n")
    console.print(Panel(
        Markdown(response_text),
        title="[bold green]Gemini Response[/bold green]",
        border_style="green",
        expand=False
    ))

def show_details(model, temperature, token_count, elapsed_time, response):
    """Display detailed information as a tree"""
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

def show_completion_time(start_time):
    """Display the total completion time"""
    elapsed = time.time() - start_time
    console.rule(f"[bold purple]Completed in {elapsed:.2f} seconds[/bold purple]")