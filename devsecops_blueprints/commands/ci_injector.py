import typer
import os
import time
from rich.progress import Progress, SpinnerColumn, TextColumn
from devsecops_blueprints.ui.console import console, print_success_panel, print_error_panel

app = typer.Typer()

@app.command("inject-ci")
def inject_ci():
    """
    Automatically creates the .github/workflows directory and injects a Zero-Trust CI/CD pipeline.
    """
    workflow_dir = ".github/workflows"
    workflow_path = os.path.join(workflow_dir, "f9-security-gate.yml")
    
    workflow_content = """name: DevSecOps Blueprints Security Scan

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

jobs:
  security-scan:
    name: Advanced Vulnerability & Audit Scan
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        
      - name: Setup Python environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          
      - name: Build & Install DevSecOps Tooling
        run: |
          curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
          curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/install.sh | sh -s -- -b /usr/local/bin
          pip install typer rich httpx
          pip install .
          
      - name: Audit Repository for Hardcoded Secrets
        run: devsecops-blueprints audit
        
      - name: Scan Infrastructure as Code (IaC)
        run: devsecops-blueprints iac .
"""

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}[/bold cyan]"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[*] Injecting Zero-Trust CI/CD pipeline...", total=None)
            time.sleep(1.5) # Sleek visual effect
            
            if not os.path.exists(workflow_dir):
                os.makedirs(workflow_dir)
                console.print(f"[i] Created directory: {workflow_dir}")
                
            with open(workflow_path, "w") as f:
                f.write(workflow_content)
                
        print_success_panel(
            "Pipeline Secured", 
            f"GitHub Action workflow saved to [bold white]{workflow_path}[/bold white].\nPull Requests will now be strictly gated."
        )
    except Exception as e:
        print_error_panel("Injection Failed", str(e))
        raise typer.Exit(1)
