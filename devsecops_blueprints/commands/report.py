import typer
import subprocess
import json
import os
import tempfile
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from devsecops_blueprints.ui.console import console, print_success_panel, print_error_panel
from devsecops_blueprints.core.report_generator import generate_html_report

app = typer.Typer()

@app.command("report")
def report_command(directory: str = typer.Argument(".", help="Directory to analyze")):
    """
    Silent operation: Generates a stunning HTML Executive Security Report.
    """
    spinner = Spinner("line", text=Text("[*] Aggregating security layers into Executive Report...", style="bold magenta"))
    
    with Live(spinner, refresh_per_second=10, console=console, transient=True):
        secrets_data = []
        iac_data = {}
        
        # 1. Run Secrets Scan Silently
        fd, temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        try:
            subprocess.run(
                ["gitleaks", "detect", "--report-format", "json", "--report-path", temp_path, "--source", directory],
                capture_output=True,
                check=False
            )
            with open(temp_path, "r") as f:
                content = f.read()
                if content.strip():
                    secrets_data = json.loads(content)
        except Exception:
            pass # Failsafe fallbacks
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        # 2. Run IaC Scan Silently
        try:
            result = subprocess.run(
                ["trivy", "config", "--format", "json", "--quiet", directory],
                capture_output=True,
                text=True,
                check=False
            )
            if result.stdout.strip():
                iac_data = json.loads(result.stdout)
        except Exception:
            pass
            
        # Generate the report
        output_file = generate_html_report(secrets_data, iac_data)
        
    print_success_panel(
        "Report Generated",
        f"Executive summary successfully exported to [bold cyan]{output_file}[/bold cyan].\nOpen this file in your web browser."
    )
