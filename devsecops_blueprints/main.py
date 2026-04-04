import typer
from devsecops_blueprints.ui.console import print_logo
from devsecops_blueprints.commands import scan, fetch, audit, setup, ci_injector, iac, catalog, report, remediate

# We use rich formatting inside help
app = typer.Typer(
    help="DevSecOps Blueprints: The ultimate enterprise CLI for vulnerability scanning and patching.",
    no_args_is_help=True,
    rich_markup_mode="rich"
)

@app.callback()
def main():
    """
    Intercepts the execution to draw the visually stunning ASCII art.
    """
    print_logo()

app.command(name="scan")(scan.scan_command)
app.command(name="fetch")(fetch.fetch_command)
app.command(name="audit")(audit.audit_command)
app.command(name="setup")(setup.setup_command)
app.command(name="inject-ci")(ci_injector.inject_ci)
app.command(name="iac")(iac.iac_command)
app.command(name="catalog")(catalog.catalog_command)
app.command(name="report")(report.report_command)
app.command(name="fix")(remediate.fix_command)

if __name__ == "__main__":
    app()
