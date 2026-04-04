import typer
import subprocess
import json
from rich.spinner import Spinner
from rich.live import Live
from devsecops_blueprints.ui.console import console, print_error_panel, create_table, print_success_panel
from rich.text import Text

app = typer.Typer()

@app.callback(invoke_without_command=True)
def _default():
    pass

@app.command("iac")
def iac_command(directory: str = typer.Argument(".", help="Directory to scan")):
    """
    Scans Infrastructure as Code (Terraform, Dockerfile, K8s) for misconfigurations.
    """
    spinner = Spinner("line", text=Text("[*] Analyzing IaC files for misconfigurations...", style="bold white"))
    
    with Live(spinner, refresh_per_second=10, console=console, transient=True):
        try:
            result = subprocess.run(
                ["trivy", "config", "--format", "json", "--quiet", directory],
                capture_output=True,
                text=True,
                check=False
            )
        except FileNotFoundError:
            print_error_panel("Dependency Missing", "Trivy is not installed or not in PATH.")
            raise typer.Exit(1)
            
    if result.returncode != 0 and not result.stdout.strip():
        print_error_panel("IaC Scan Failed", result.stderr)
        raise typer.Exit(1)
        
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print_success_panel("Clean Infrastructure", "No IaC misconfigurations detected.")
        return
        
    misconfigs = []
    if "Results" in data:
        for res in data["Results"]:
            target = res.get("Target", "Unknown File")
            for vuln in res.get("Misconfigurations", []):
                severity = vuln.get("Severity", "")
                if severity in ["HIGH", "CRITICAL"]:
                    misconfigs.append({
                        "File": target,
                        "Type": vuln.get("Type", "Config"),
                        "Message": vuln.get("Message", ""),
                        "Severity": severity
                    })
                    
    if not misconfigs:
        print_success_panel("Secure Infrastructure", "No HIGH or CRITICAL IaC misconfigurations found.")
        return
        
    table = create_table("Infrastructure Misconfigurations Detected", ["File", "Type", "Issue", "Severity"])
    
    for cfg in misconfigs:
        severity_col = f"[bold red]{cfg['Severity']}[/bold red]" if cfg['Severity'] == "CRITICAL" else f"[bold yellow]{cfg['Severity']}[/bold yellow]"
        
        table.add_row(
            f"[info]{cfg['File']}[/info]",
            cfg['Type'],
            cfg['Message'],
            severity_col
        )
        
    console.print(table)
