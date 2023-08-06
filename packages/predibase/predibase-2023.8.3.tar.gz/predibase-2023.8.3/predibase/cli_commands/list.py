from typing import Optional

import typer
from rich.table import Table

from predibase.cli_commands.utils import get_client, get_console, get_repo

app = typer.Typer()


@app.command()
def models(repo: Optional[str] = None):
    repo = get_repo(repo)
    table = Table("Version", "Description", "UUID")
    for model in repo.list_models():
        table.add_row(str(model.version), model.description, model.uuid)
    get_console().print(table)


@app.command()
def repos():
    table = Table("Name", "UUID")
    repos = get_client().list_model_repos()
    for repo in repos:
        table.add_row(repo.name, repo.uuid)
    get_console().print(table)


if __name__ == "__main__":
    app()
