import typer
import subprocess
import json
import os
import tempfile
from rich.spinner import Spinner
from rich.live import Live
from devsecops_blueprints.ui.console import console, print_error_panel, create_table, print_success_panel
from rich.text import Text

app = typer.Typer()

@app.callback(invoke_without_command=True)
def _default():
    pass

@app.command("audit")
def audit_command():
    """
    Audits the local repository for hardcoded secrets.
    """
    spinner = Spinner("line", text=Text("[*] Scanning directory for exposed secrets...", style="bold white"))
    
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    with Live(spinner, refresh_per_second=10, console=console, transient=True):
        try:
            result = subprocess.run(
                ["gitleaks", "detect", "-v", "--report-format", "json", "--report-path", temp_path],
                capture_output=True,
                text=True,
                check=False
            )
        except FileNotFoundError:
            os.remove(temp_path)
            print_error_panel("Missing Dependency", "Gitleaks is not installed or not in system PATH. Install it to enable local auditing.")
            raise typer.Exit(1)

    try:
        with open(temp_path, "r") as f:
            content = f.read()
            if not content.strip():
                data = [] # empty
            else:
                data = json.loads(content)
    except json.JSONDecodeError:
        data = []
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    if not data:
        print_success_panel("Clean Directory!", "Your armory is secure. No hardcoded secrets were detected.")
        return
        
    table = create_table("[!] Secret Leakage Detected", ["File", "Rule", "Secret Match", "Severity"])
    
    for leak in data:
        file_loc = f"{leak.get('File', 'Unknown')}:{leak.get('StartLine', '?')}"
        severity = leak.get("Severity", "CRITICAL").upper()
        sev_color = "bold red" if severity in ["CRITICAL", "HIGH"] else "bold yellow"
        
        # Redact the secret explicitly
        secret = leak.get("Secret", "")
        if len(secret) > 6:
            secret = secret[:3] + "..." + secret[-3:]
        else:
            secret = "***"
            
        table.add_row(
            f"[info]{file_loc}[/info]",
            leak.get('RuleID', 'Unknown'),
            f"[prompt]{secret}[/prompt]",
            f"[{sev_color}]{severity}[/{sev_color}]"
        )
        
    console.print(table)
    
    from devsecops_blueprints.ui.console import print_actionable_solution
    print_actionable_solution("Secrets must be completely scrubbed via git filter-repo or similar tools.\nStore them in a secure vault.")
