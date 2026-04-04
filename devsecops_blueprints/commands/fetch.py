import typer
from typing import Optional
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, DownloadColumn
from devsecops_blueprints.ui.console import console, print_error_panel, print_success_panel
from devsecops_blueprints.core.github_client import stream_blueprint
from devsecops_blueprints.commands.catalog import display_catalog

app = typer.Typer()

@app.callback(invoke_without_command=True)
def _default():
    pass

@app.command("fetch")
def fetch_command(template_name: Optional[str] = typer.Argument(None)):
    """
    Fetches a secure-by-default template blueprint.
    """
    if template_name is None:
        display_catalog()
        template_name = Prompt.ask("\n[bold magenta][*] Enter the name of the blueprint to equip[/bold magenta]")
        
    dest_path = "Dockerfile"
    
    try:
        with Progress(
            SpinnerColumn("line"),
            TextColumn("[bold white]{task.description}"),
            BarColumn(bar_width=40, style="cyan", complete_style="green"),
            DownloadColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[*] Initiating secure link to F9 Armory...", total=None)
            
            with open(dest_path, "wb") as f:
                for chunk, chunk_size, total_size in stream_blueprint(template_name):
                    if progress.tasks[task].total is None and total_size > 0:
                        progress.update(task, total=total_size)
                    
                    f.write(chunk)
                    progress.update(task, advance=chunk_size)
                    
        print_success_panel("Armor Equipped", f"Secure blueprint for [bold white]{template_name}[/bold white] injected successfully. You are now shielded.")
        
    except ValueError as val_err:
        print_error_panel("Retrieval Failed", str(val_err))
        raise typer.Exit(1)
    except ConnectionError as conn_err:
        print_error_panel("Network Offline", str(conn_err))
        raise typer.Exit(1)
    except Exception as e:
        print_error_panel("Critical Error", str(e))
        raise typer.Exit(1)
