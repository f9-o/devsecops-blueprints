import typer
from rich.tree import Tree
from devsecops_blueprints.ui.console import console

app = typer.Typer()

def display_catalog():
    """Builds and displays the highly structured, categorized list of blueprints."""
    tree = Tree("[bold cyan]F9 Armory Blueprint Catalog[/bold cyan]")
    
    docker_node = tree.add("[bold magenta][ Docker Environments ][/bold magenta]")
    docker_node.add("[bold white]docker-node[/bold white] - Hardened Node.js image")
    docker_node.add("[bold white]docker-python[/bold white] - Secure Python 3.10 distroless image")
    
    ci_node = tree.add("[bold magenta][ CI/CD Pipelines ][/bold magenta]")
    ci_node.add("[bold white]github-actions-gate[/bold white] - Full DevSecOps PR Blocking")
    ci_node.add("[bold white]gitlab-security[/bold white] - SAST & Secret Scanning Pipeline")

    k8s_node = tree.add("[bold magenta][ Kubernetes Policies ][/bold magenta]")
    k8s_node.add("[bold white]k8s-baseline[/bold white] - Restrictive Pod Security Admission")
    k8s_node.add("[bold white]network-deny-all[/bold white] - Default deny-all ingress/egress")

    iac_node = tree.add("[bold magenta][ IaC Modules ][/bold magenta]")
    iac_node.add("[bold white]tf-aws-secure-vpc[/bold white] - AWS VPC with FlowLogs and strict SG")

    console.print()
    console.print(tree)
    console.print()

@app.command("catalog")
def catalog_command():
    """
    Displays a highly structured, categorized list of available secure blueprints.
    """
    display_catalog()
