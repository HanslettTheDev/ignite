"""This module provides the CLI for Ignite"""
# ignite/cli.py

import typer
from pathlib import Path
from typing import Dict, Optional, Any
from typing_extensions import Annotated
from ignite import ( ERRORS, __app_name__, __version__, config, 
    database, PROMPT_MESSAGES
)

from ignite.ignite import Igniter

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_PATH),
        "--db-path",
        "-db",
        prompt="ignite database location?",
        ),
    ) -> None:
    
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    db_init_error = database.create_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The ignite database path is {db_path}", fg=typer.colors.GREEN)


def setup_igniter() -> Igniter:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "ignite init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return Igniter(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "ignite init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def add() -> None:
    igniter = setup_igniter()
    responses = []
    for i in range(0, len(PROMPT_MESSAGES)):
        prompt = typer.prompt(PROMPT_MESSAGES[i])
        if igniter.check_data(prompt, i):
            responses.append(prompt)
            continue
        typer.secho(f"Sorry! data not recognized", fg=typer.colors.RED)
        raise typer.Exit(1)


    igniter.add(responses)

    typer.secho(
        f"Added project **{responses[0]}** successfully", 
        fg=typer.colors.GREEN
    )

@app.command()
def launch(
        project_name: Annotated[str, typer.Argument(help="A valid project name as found in your ignite settings")]
    ) -> None:

    import subprocess

    igniter = setup_igniter()
    read_data = igniter._db_handler.read_ignite_settings()
    
    data = {}

    for pj in read_data.ignite_settings:
        try:
            if pj[project_name]:
                data = pj
                break
        except KeyError:
            continue

    if not data:
        typer.secho(
            f"Project *{project_name}* doesn't exists! Create one using 'ignite add'", 
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    subprocess.Popen(
        f'start cmd /K "{data[project_name]["code_editor"]} "{data[project_name]["folder_location"]}""', 
        shell=True
    )

    typer.secho(
        f"Project {project_name} successfully launched in {data[project_name]['code_editor']}!", 
        fg=typer.colors.GREEN
    )

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
    ) -> None:
    return
