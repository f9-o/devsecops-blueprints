import typer
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from devsecops_blueprints.ui.console import console, print_error_panel, create_table, print_actionable_solution
from devsecops_blueprints.core.trivy_engine import run_trivy_scan

app = typer.Typer()

@app.callback(invoke_without_command=True)
def _default():
    pass

@app.command("scan")
def scan_command(image_name: str):
    """
    Scans a container image for high and critical vulnerabilities.
    """
    spinner = Spinner("line", text=Text("[*] Analyzing layers and searching for vulnerabilities...", style="bold white"))
    
    with Live(spinner, refresh_per_second=10, console=console, transient=True):
        try:
            results = run_trivy_scan(image_name)
        except Exception as e:
            print_error_panel("Scan Failed", str(e))
            raise typer.Exit(1)
            
    if not results:
        from devsecops_blueprints.ui.console import print_success_panel
        print_success_panel("Clean Image", f"No HIGH or CRITICAL vulnerabilities found in {image_name}.")
        return

    # Results found
    table = create_table(f"Scan Results for [bold yellow]{image_name}[/bold yellow]", ["Layer ID", "Target", "Vulnerability", "Severity", "Fixed Version"])
    
    for vuln in results:
        severity_col = f"[bold red]{vuln['Severity']}[/bold red]" if vuln['Severity'] == "CRITICAL" else f"[bold yellow]{vuln['Severity']}[/bold yellow]"
        
        table.add_row(
            f"[layer]{vuln['Layer ID']}[/layer]",
            vuln['Target'],
            vuln['Vulnerability'],
            severity_col,
            f"[bold green]{vuln['Fixed Version']}[/bold green]"
        )
        
    console.print(table)
    print_actionable_solution(f"Stop patching endlessly. Start secure.\nRun [prompt]devsecops-blueprints fetch <template>[/prompt] to get our hardened baseline.")
