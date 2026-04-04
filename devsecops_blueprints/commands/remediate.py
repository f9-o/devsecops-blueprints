import typer
from rich.prompt import Confirm
from devsecops_blueprints.ui.console import console, print_success_panel, print_error_panel, create_table
from devsecops_blueprints.core.patch_engine import run_auto_patcher

app = typer.Typer()

@app.command("fix")
def fix_command(directory: str = typer.Argument(".", help="Directory to auto-patch")):
    """
    Parses your IaC/Docker files and automatically rewrites them with secure-by-default logic.
    """
    console.print("\n[bold cyan][*] Initiating Zero-Trust Auto-Remediation Engine...[/bold cyan]")
    
    do_patch = Confirm.ask("\n[bold magenta]This will modify your source files. Proceed with auto-patching?[/bold magenta]", default=True)
    
    if not do_patch:
        console.print("[dim white]Operation aborted.[/dim white]")
        raise typer.Exit()
        
    patches = run_auto_patcher(directory)
    
    if not patches:
        print_success_panel("Zero-Trust Verified", "No insecure patterns were found that required patching.")
        return
        
    table = create_table("Security Patches Applied", ["File Patched", "Action Taken"])
    for p in patches:
        table.add_row(f"[info]{p['File']}[/info]", f"[bold green]{p['Action']}[/bold green]")
        
    console.print(table)
    print_success_panel("Remediation Complete", f"Successfully secured {len(patches)} configurations.")
