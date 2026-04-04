import typer
import platform
import subprocess
from rich.table import Table
from rich.prompt import Confirm
from devsecops_blueprints.ui.console import console, print_error_panel, print_success_panel

app = typer.Typer()

@app.callback(invoke_without_command=True)
def _default():
    pass

@app.command("setup")
def setup_command():
    """
    Shows installation instructions and attempts to install DevSecOps tools (Trivy, Gitleaks).
    """
    os_name = platform.system()
    
    table = Table(title="Required DevOps Tooling Installation", show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Tool")
    table.add_column("macOS (Homebrew)")
    table.add_column("Windows (Winget)")
    table.add_column("Linux (Apt / Shell)")
    
    table.add_row("Trivy", "brew install trivy", "winget install Aquasecurity.Trivy", "curl -sfL .../install.sh | sh")
    table.add_row("Gitleaks", "brew install gitleaks", "winget install gitleaks", "curl -sSfL .../install.sh | sh")
    
    console.print("\n")
    console.print(table)
    console.print("\n[info]To ensure maximum capability, these dependencies must be available in your PATH.[/info]\n")
    
    if os_name == "Windows":
        if Confirm.ask("Would you like to auto-install them now using Winget?"):
            console.print("\n[bold cyan]Installing Trivy...[/bold cyan]")
            subprocess.run(["winget", "install", "Aquasecurity.Trivy"], check=False)
            
            console.print("\n[bold cyan]Installing Gitleaks...[/bold cyan]")
            subprocess.run(["winget", "install", "gitleaks"], check=False)
            
            print_success_panel("Setup Complete", "Please restart your terminal to ensure PATH changes take effect.")
