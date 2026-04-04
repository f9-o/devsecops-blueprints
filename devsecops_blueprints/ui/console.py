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
    """Prints a clear and readable ASCII Art Logo."""
    logo = r"""[bold cyan]
  ___ ___   ___ _    _   _ ___ ___ ___ ___ _  _ _____ ___ 
 | __/ _ \ | _ ) |  | | | | __| _ \ _ \_ _| \| |_   _/ __|
 | _| (_) || _ \ |__| |_| | _||  _/   /| || .` | | | \__ \
 |_| \___/ |___/____|\___/|___|_| |_|_\___|_|\_| |_| |___/[/bold cyan]
             [bold magenta]S E C U R E  A R M O R Y[/bold magenta]
    """
    console.print(logo, justify="center")

def print_success_panel(title: str, content: str):
    """Displays a visually distinct success message wrapped in a rounded panel."""
    panel = Panel(
        content, 
        title=f"[[bold green]+[/bold green]] {title}", 
        border_style="bold green", 
        expand=False,
        padding=(1, 2)
    )
    console.print(panel)

def print_error_panel(title: str, content: str):
    """Displays critical errors with a bold red panel."""
    panel = Panel(
        content, 
        title=f"[[bold red]![/bold red]] {title}", 
        border_style="bold red", 
        expand=False,
        padding=(1, 2)
    )
    console.print(panel)

def print_actionable_solution(message: str):
    """The 'Magic Hook' panel to redirect users to use blueprints."""
    panel = Panel(
        f"[bold white]{message}[/]", 
        title="[[bold yellow]>[/bold yellow]] ACTION ITEM", 
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
