import typer
import os
from devsecops_blueprints.ui.console import console, print_success_panel, print_error_panel

app = typer.Typer()

@app.callback(invoke_without_command=True)
def _default():
    pass

@app.command("inject-ci")
def inject_ci():
    """
    Injects a carefully crafted GitHub Actions workflow for continuous DevSecOps scanning.
    """
    workflow_dir = ".github/workflows"
    workflow_path = os.path.join(workflow_dir, "blueprints-security.yml")
    
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
        if not os.path.exists(workflow_dir):
            os.makedirs(workflow_dir)
            console.print(f"[[dim]info[/dim]] Created directory: {workflow_dir}")
            
        with open(workflow_path, "w") as f:
            f.write(workflow_content)
            
        print_success_panel(
            "CI/CD Injected Successfully", 
            f"GitHub Action workflow saved to [bold white]{workflow_path}[/bold white].\nYour repository is now secured on every push!"
        )
    except Exception as e:
        print_error_panel("Injection Failed", str(e))
        raise typer.Exit(1)
