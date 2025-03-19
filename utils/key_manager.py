from dotenv import load_dotenv
import os
from rich.console import Console

class ApiKeyManager:
    """
    Class to manage API keys and environment variables
    """
    def __init__(self, required_keys=None, console=None):
        """
        Initialize the API key manager
        
        Args:
            required_keys (list): List of required API key names
            console (Console): Optional Rich console for output
        """
        self.console = console or Console()
        self.required_keys = required_keys or []
        self.keys = {}
        self._load_env_vars()
    
    def _load_env_vars(self):
        """Load environment variables from .env file"""
        with self.console.status("[bold blue]Loading environment variables...", spinner="dots"):
            load_dotenv()
            self.console.print("[bold green]Environment variables loaded![/bold green]")
            
            # Load all required keys
            missing_keys = []
            for key_name in self.required_keys:
                value = os.getenv(key_name)
                if not value:
                    missing_keys.append(key_name)
                else:
                    self.keys[key_name] = value
            
            # Report any missing keys
            if missing_keys:
                missing_keys_str = ", ".join(missing_keys)
                error_msg = f"Required keys not found: {missing_keys_str}. Please check your .env file."
                self.console.print(f"[bold red]Error:[/bold red] {error_msg}", style="bold red")
                raise ValueError(error_msg)
            else:
                self.console.print("[bold green]All required API keys loaded successfully![/bold green]")
    
    def get(self, key_name):
        """Get an API key or environment variable by name"""
        if key_name in self.keys:
            return self.keys[key_name]
        
        # Try to get from environment if not already loaded
        value = os.getenv(key_name)
        if value:
            self.keys[key_name] = value
            return value
        
        self.console.print(f"[bold yellow]Warning:[/bold yellow] Key '{key_name}' not found", style="yellow")
        return None