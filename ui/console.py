from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table

# Sleek Hacker/Cyberpunk theme for premium CLI aesthetics
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "danger": "bold red",
    "success": "bold green",
    "prompt": "bold magenta",
    "layer": "dim white"
})

console = Console(theme=custom_theme)

def print_logo():
    """Prints a mathematically striking gradient or dual-tone ASCII Art Logo."""
    logo = r"""
    
    ____             _____            ____            
   / __ \___ _   __ / ___/___  _____ / __ \____  _____
  / / / / _ \ | / / \__ \/ _ \/ ___// / / / __ \/ ___/
 / /_/ /  __/ |/ / ___/ /  __/ /__ / /_/ / /_/ (__  ) 
/_____/\___/|___/ /____/\___/\___/ \____/ .___/____/  
                                       /_/            
     [bold cyan]B L U E P R I N T S[/bold cyan] [dim]»[/dim] [bold magenta]S E C U R E  A R M O R Y[/bold magenta]
    """
    console.print(logo, justify="center")

def print_success_panel(title: str, content: str):
    """Displays a visually distinct success message wrapped in a rounded panel."""
    panel = Panel(
        content, 
        title=f"✅ {title}", 
        border_style="bold green", 
        expand=False,
        padding=(1, 2)
    )
    console.print(panel)

def print_error_panel(title: str, content: str):
    """Displays critical errors with a bold red panel."""
    panel = Panel(
        content, 
        title=f"🚨 {title}", 
        border_style="bold red", 
        expand=False,
        padding=(1, 2)
    )
    console.print(panel)

def print_actionable_solution(message: str):
    """The 'Magic Hook' panel to redirect users to use blueprints."""
    panel = Panel(
        f"[bold white]{message}[/]", 
        title="💡 Actionable Solution", 
        border_style="bold yellow", 
        expand=False,
        padding=(1, 3)
    )
    console.print("\n", panel, justify="center")

def create_table(title: str, columns: list[str]) -> Table:
    """Helper to maintain a consistent sleek table design throughout the CLI."""
    table = Table(
        title=f"\n[bold white]{title}[/bold white]\n",
        show_header=True, 
        header_style="bold magenta", 
        expand=True,
        border_style="cyan",
        title_justify="left"
    )
    for col in columns:
        table.add_column(col)
    return table
